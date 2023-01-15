function PuckCaller(TifDir, OutDir, NumPar)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%TifDir = 'tmp/files';
%OutDir = 'tmp/out';
%NumPar = '12'; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
NumPar = str2num(NumPar); 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

PixelThreshold = 30;
BaseBalanceTolerance = 0.05;
Cy3TxRMixing = 0.0;
BeadSizeThreshold = 30;
NumSkippedBases = 0;
BeadZeroThreshold = 1;
ImageSize = 5120;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ChannelNum = 4;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

directory = dir( fullfile(TifDir, '*_zselect.tif') );
files = { directory.name };
files = sort(files);
files = string(files);

Puck = char( regexprep( files(1) , '_.*' , '' ) );

for i = 1:length(files)
	basenames(i) = regexprep(files(i), '_zselect.tif', '');
	paths(i) = fullfile(TifDir, files(i));
end

basenames = string(basenames);
paths = string(paths);

n = length(files);
NumBases = n;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

info = imfinfo(paths(1));
ROI = [ [1,info.Height] ; [1,info.Width] ];
ROIHeight = ROI(1,2) - ROI(1,1) + 1;
ROIWidth = ROI(2,2) - ROI(2,1) + 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fileID = fopen( fullfile(OutDir, [Puck, '_offsets.csv']) , 'w' );
fprintf(fileID, 'Ligation,Channel,x,y\n');
fprintf(fileID, '%d,%d,%d,%d\n', 1, 1, 0, 0);
fprintf(fileID, '%d,%d,%d,%d\n', 1, 2, 0, 0);
fprintf(fileID, '%d,%d,%d,%d\n', 1, 3, 0, 0);
fprintf(fileID, '%d,%d,%d,%d\n', 1, 4, 0, 0);

for l = 1:n

	mapOrigstack = imread(paths(l));

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	ImageOut = zeros( size(mapOrigstack) , 'uint16' );
	ImageOut(:,:,1) = mapOrigstack(:,:,1);

	b = [ 1200 , 1700 , 1200 , 1700 ];
   
	imBinMap(:,:) = mapOrigstack(b(1):b(2),b(3):b(4),1) > median( median( mapOrigstack(:,:,1)) );

	for c = 2:size(mapOrigstack,3)
		disp( ['Channel ', num2str(c)] );
		imBinChannel = mapOrigstack(b(1):b(2),b(3):b(4),c) > median( median( mapOrigstack(:,:,c) ) );
		Cor = xcorr2( uint8(imBinMap) , uint8(imBinChannel) );
		[ssr,snd] = max( Cor(:) );
		[y,x] = ind2sub( size(Cor) , snd );
		offset = [ -((b(4)-b(3)+1-x)) , -(b(2)-b(1)+1-y) ];
		disp(offset);
		fprintf(fileID, '%d,%d,%d,%d\n', l, c, offset(1), offset(2));
		ImageOut(:,:,c) = uint16( imtranslate( mapOrigstack(:,:,c) , offset ) );
	end

	for c = 1:ChannelNum
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_offset.tif'));
		disp(OutPath);
		imwrite(ImageOut(:,:,c), OutPath);
	end

	for c = 1:ChannelNum
		mapstack(:,:,c) = im2single( imadjust( ImageOut(:,:,c) ) );
	end

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% save matrix
	OutPath = fullfile(OutDir, strcat(basenames(l), '_adjust.mat'));
	VarName = ['Adjust', num2str(l)];
	eval([VarName, ' = mapstack;']);
	save(OutPath, VarName);

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% save channel-separated tif files
	for c = 1:ChannelNum
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_adjust.tif'));
		disp(OutPath);
		imwrite(uint16(mapstack(:,:,c)), OutPath);
	end

end

fclose(fileID);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

scaleFactorDown = 1;

% load first ligation
LigationPath1 = fullfile(OutDir, strcat(basenames(1), '_adjust.mat'));
load(LigationPath1);

map = max(Adjust1, [], 3);
map1 = imresize(map, scaleFactorDown);

for c = 1:ChannelNum
	TifPath = fullfile(OutDir, strcat(basenames(1), '_channel', num2str(c), '_offset.tif'));
	mapOrigstack(:,:,c) = imread(TifPath);
end

% save matrix
OutPath = fullfile(OutDir, strcat(basenames(1), '_transform.mat'));
disp(OutPath);
VarName = 'Transform1'
eval([VarName, ' = mapOrigstack;']);
save(OutPath, VarName);

% save channel-separated tif files
for c = 1:ChannelNum
	OutPath = fullfile(OutDir, strcat(basenames(1), '_channel', num2str(c), '_transform.tif'));
	disp(OutPath);
	imwrite(mapOrigstack(:,:,c), OutPath);
end


for l = 2:n

	LigationPath = fullfile(OutDir, strcat(basenames(l), '_adjust.mat'));
	VarName = ['Adjust', num2str(l)];
	load(LigationPath, VarName);
	eval( ['querystack = ' , VarName , ';' ] );

	query = max(querystack(:,:,:), [], 3);
	query1 = imresize(query, scaleFactorDown);
		    
	tformEstimate = imregcorr(query1, map1);

	disp(tformEstimate.T);
	OutPath = fullfile(OutDir, strcat(basenames(l), '_transform.csv'));
	disp(OutPath);
	csvwrite(OutPath, tformEstimate.T);

	tformEstimate.T(3,1) = tformEstimate.T(3,1) / scaleFactorDown;
	tformEstimate.T(3,2) = tformEstimate.T(3,2) / scaleFactorDown;
	Rfixed = imref2d( size(map) );

	for c = 1:ChannelNum
		TifPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_offset.tif'));
		queryOrigstack(:,:,c) = imread(TifPath);
	end

	for c = 1:4
		final = imwarp( squeeze( queryOrigstack(:,:,c) ) , tformEstimate , 'OutputView' , Rfixed );
		final = final(1:ImageSize ,1:ImageSize);
		transformOut(:,:,c) = final;
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_transform.tif'));
		disp(OutPath);
		imwrite(final, OutPath);
	end

	OutPath = fullfile(OutDir, strcat(basenames(l), '_transform.mat'));
	disp(OutPath);
	VarName = ['Transform', num2str(l)]
	eval([VarName, ' = transformOut;']);
	save(OutPath, VarName);

	OutPath = fullfile(OutDir, strcat(basenames(l), '_transform.tif'));
	disp(OutPath);
	imwrite(transformOut(:,:,1), OutPath);
	for c = 2:size(transformOut,3)
		imwrite(transformOut(:,:,c), OutPath, 'WriteMode', 'append');
	end

end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


puckimage = zeros(ROIHeight, ROIWidth, ChannelNum);

for l = 1:n

	LigationPath = fullfile(OutDir, strcat(basenames(l), '_transform.mat'));
	VarName = ['Transform', num2str(l)];
	load(LigationPath, VarName);
	eval( ['puckimage = ' , VarName , ';' ] );
	puckimage = double(puckimage);
    
    unsubtracted = puckimage;

	for c = 1:ChannelNum
		tempimage = puckimage(:,:,c);
		SE = strel('ball', 50, 30);
		J = imtophat(tempimage, SE);
		puckimage(:,:,c) = J;
     end

	OutPath = fullfile(OutDir, strcat(basenames(l), '_tophat.mat'));
	disp(OutPath);
	VarName = ['Tophat', num2str(l)]
	eval([VarName, ' = puckimage;']);
	save(OutPath, VarName);

	for c = 1:ChannelNum
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_tophat.tif'));
		disp(OutPath);
		imwrite(uint16(puckimage(:,:,c)), OutPath);
	end

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for l = 1:n

	LigationPath = fullfile(OutDir, strcat(basenames(l), '_tophat.mat'));
	VarName = ['Tophat', num2str(l)];
	load(LigationPath, VarName);
	eval( ['puckimage = ' , VarName , ';' ] );
	puckimage = double(puckimage);
    
	channel3 = im2single( puckimage(:,:,3) );
	channel2 = im2single( puckimage(:,:,2) );

	threshidx = find( channel2 > 10000 );
	scatter( channel2(threshidx) , channel3(threshidx) );
	p = polyfit( channel2(threshidx) , channel3(threshidx) , 1 );

	puckimage(:,:,3) = (puckimage(:,:,3) - Cy3TxRMixing * puckimage(:,:,2) );

	OutPath = fullfile(OutDir, strcat(basenames(l), '_mixing.mat'));
	disp(OutPath);
	VarName = ['Mixing', num2str(l)]
	eval([VarName, ' = puckimage;']);
	save(OutPath, VarName);

	for c = 1:ChannelNum
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_mixing.tif'));
		disp(OutPath);
		imwrite(uint16(puckimage(:,:,c)), OutPath);
	end

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fileID = fopen( fullfile(OutDir, [Puck, '_multipliers.csv']) , 'w' );
fprintf(fileID, 'Ligation,Channel1,Channel2,Channel3,Channel4\n');

for l = 1:n


	LigationPath = fullfile(OutDir, strcat(basenames(l), '_mixing.mat'));
	VarName = ['Mixing', num2str(l)];
	load(LigationPath, VarName);
	eval( ['puckimage = ' , VarName , ';' ] );
	puckimage = double(puckimage);

	Counter = 0;
	multiplier = [1 1 1 1];

	TestImage = puckimage( (round(ROIHeight/2)-500) : (round(ROIHeight/2)+500) , (round(ROIWidth/2)-500) : (round(ROIWidth/2)+500) , : );
	        
	while true

		Counter = Counter + 1;

		if Counter>1000
			disp(['Terminating Base Balance Enforcement for Ligation ',num2str(l),' -- base balance was not obtained.']);
			break;
		end

		for c = 1:ChannelNum
			tmppuckimage(:,:,c) = multiplier(c) * TestImage(:,:,c);
	    end

		[TestM,TestI] = max(tmppuckimage, [], 3);
		TestI( TestM < PixelThreshold ) = 0;

		for c = 1:4
			BaseBalance(c) = nnz( TestI == c );
		end

		if ( max(BaseBalance) - min(BaseBalance) ) / sum(BaseBalance) > BaseBalanceTolerance
			multiplier( BaseBalance == min(BaseBalance) ) = multiplier( BaseBalance == min(BaseBalance) ) + 0.05;
		else
			disp(['Terminating Base Balance Enforcement for Ligation ',num2str(l),' after ',num2str(Counter-1),' adjustments.'])
			multiplier
			break;
		end
	end

	for c=1:ChannelNum
		puckimage(:,:,c) = multiplier(c) * puckimage(:,:,c);
	end

	fprintf(fileID, '%s,%.2f,%.2f,%.2f,%.2f\n', num2str(l), multiplier(1), multiplier(2), multiplier(3), multiplier(4));

	OutPath = fullfile(OutDir, strcat(basenames(l), '_balanced.mat'));
	disp(OutPath);
	VarName = ['Balanced', num2str(l)]
	eval([VarName, ' = puckimage;']);
	save(OutPath, VarName);

	for c = 1:ChannelNum
		OutPath = fullfile(OutDir, strcat(basenames(l), '_channel', num2str(c), '_balanced.tif'));
		disp(OutPath);
		imwrite(uint16(puckimage(:,:,c)), OutPath);
    end

end

fclose(fileID);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for l = 1:n

	LigationPath = fullfile(OutDir, strcat(basenames(l), '_balanced.mat'));
	VarName = ['Balanced', num2str(l)];
	load(LigationPath, VarName);
	eval( ['puckimage = ' , VarName , ';' ] );
	puckimage = double(puckimage);

	[M,I] = max(puckimage, [], 3);

	I( M < PixelThreshold ) = 0;
	Indices(:,:,l) = uint8(I);
    
end

OutPath = fullfile(OutDir, [Puck, '_indices.tif']);
disp(OutPath);
imwrite(Indices(:,:,1), OutPath);
for l = 2:n
	imwrite(Indices(:,:,l), OutPath, 'WriteMode', 'append');
end
for l = 1:n
	OutPath = fullfile(OutDir, strcat(basenames(l), '_indices.tif'));
	disp(OutPath);
	imwrite(Indices(:,:,l), OutPath);
end

OutPath = fullfile(OutDir, [Puck, '_indices.mat']);
disp(OutPath);
save(OutPath, 'Indices');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

IndicesPath = fullfile(OutDir, [Puck, '_indices.mat']);
load(IndicesPath);


FlattenedBarcodes = uint64( zeros(ROIHeight, ROIWidth) );

for l = 1:n
	disp(['Ligation ', num2str(l)]);
	FlattenedBarcodes = FlattenedBarcodes + uint64( Indices(:,:,l) ) * 5^(l-1);
end

PresentBarcodes = unique(FlattenedBarcodes);
BarcodeOccCounts = histogram(FlattenedBarcodes,PresentBarcodes);
manypixelbarcodeswithzeros = PresentBarcodes( BarcodeOccCounts.Values > BeadSizeThreshold );

BaseBalanceBarcodes =manypixelbarcodeswithzeros( cellfun( @numel , strfind( string( dec2base( manypixelbarcodeswithzeros , 5 , (l-NumSkippedBases) ) ) , '0' ) ) <= 7 );

%The base 5 representations of the basecalls are:
BaseBalanceBase5Barcodes = cellfun( @(x) reverse(string(x)) , { dec2base( BaseBalanceBarcodes , 5 , (l-NumSkippedBases) ) } , 'UniformOutput', false );

BaseBalanceBase5Barcodes = BaseBalanceBase5Barcodes{1};

manypixelbarcodestmp = manypixelbarcodeswithzeros( cellfun( @numel, strfind( string( dec2base( manypixelbarcodeswithzeros , 5 , (l-NumSkippedBases) ) ) ,'0' ) ) <= BeadZeroThreshold );

manypixelbarcodes = zeros( 1 , ceil( length(manypixelbarcodestmp) / NumPar ) * NumPar );
manypixelbarcodes( 1:length(manypixelbarcodestmp) ) = manypixelbarcodestmp; %We have to be careful here to get the indexing right


disp(['There are ',num2str(length(manypixelbarcodestmp)),' barcodes passing filter.']);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

BeadImage = false(ROIHeight, ROIWidth);

totalbarcodes = 0;

delete( gcp('nocreate') );
pool = parpool(NumPar, 'IdleTimeout', Inf);

manypixelbarcodesforpar = reshape( manypixelbarcodes , ceil( length(manypixelbarcodes) / NumPar ) , NumPar );

BeadBarcodeCell={};
BeadLocationCell={};
BeadPixCell={};

parfor parnum=1:NumPar

	pp = 0;

	disp(parnum)

	LocalManyPixelBarcodes = manypixelbarcodesforpar(:,parnum);
	LocalBeadImage = false(ROIHeight, ROIWidth);
	LocalBeadBarcodes = zeros( 1 , nnz(manypixelbarcodes(:,parnum)) );
	LocalBeadLocations = zeros( 2 , nnz(manypixelbarcodes(:,parnum)) );
	LocalBeadPix = cell(1,nnz(manypixelbarcodes(:,parnum)));

	for qq = 1:nnz(manypixelbarcodesforpar(:,parnum))

		connected = bwconncomp( FlattenedBarcodes == LocalManyPixelBarcodes(qq) );
		centroids = regionprops(connected, 'Centroid');

		if max(cellfun(@numel,connected.PixelIdxList)) > BeadSizeThreshold

			for t = 1:length(connected.PixelIdxList)

				if numel(connected.PixelIdxList{t}) > BeadSizeThreshold
					LocalBeadImage(connected.PixelIdxList{t}) = true; 
					pp = pp + 1;
					LocalBeadBarcodes(pp) = LocalManyPixelBarcodes(qq);
					LocalBeadLocations(:,pp) = centroids(t).Centroid;
					LocalBeadPix{pp} = connected.PixelIdxList{t};
				end
			end
		end
	end

	imwrite( LocalBeadImage , fullfile(OutDir, ['Worker_', num2str(parnum), '_LocalBeadImage.tif']) );

	BeadBarcodeCell{parnum} = LocalBeadBarcodes;
	BeadLocationCell{parnum} = LocalBeadLocations;
	BeadPixCell{parnum} = LocalBeadPix;
end

BeadBarcodeLength = 0;

for k=1:NumPar
	BeadBarcodeLength = BeadBarcodeLength + length(BeadBarcodeCell{k});
end

BeadBarcodes = zeros(1, BeadBarcodeLength);
BeadLocations = zeros(2, BeadBarcodeLength);
BeadPixCelljoined = cell(1, BeadBarcodeLength);

delete(pool);

BeadBarcodeIndex=1;
for k=1:NumPar
	BeadBarcodes( BeadBarcodeIndex : ( BeadBarcodeIndex + length(BeadBarcodeCell{k}) - 1 ) ) = BeadBarcodeCell{k};
	BeadLocations( : , BeadBarcodeIndex : ( BeadBarcodeIndex + length(BeadBarcodeCell{k}) - 1 ) ) = BeadLocationCell{k};
	tmpcell = BeadPixCell{k};
	for ll = 1:length(BeadBarcodeCell{k})
		BeadPixCelljoined{ BeadBarcodeIndex + ll - 1 } = tmpcell{ll}; %if this is too long, we could also just make the beadpix cell array within the parfor above
	end
	BeadBarcodeIndex = BeadBarcodeIndex + length(BeadBarcodeCell{k});
	BeadImage=BeadImage + imread( fullfile(OutDir, ['Worker_', num2str(k), '_LocalBeadImage.tif']) );
end

Bead = struct( 'Barcodes', num2cell(BeadBarcodes) , 'Locations', num2cell(BeadLocations,1) , 'Pixels', BeadPixCelljoined );

for k=1:NumPar
	BeadImageToDelete = fullfile(OutDir, ['Worker_', num2str(k), '_LocalBeadImage.tif']);
	delete(BeadImageToDelete);
end

imwrite(BeadImage, fullfile(OutDir, [Puck, '_image.tif']));

BeadBarcodes = [Bead.Barcodes];
BeadLocations = {Bead.Locations};
[UniqueBeadBarcodes, BBFirstRef, BBOccCounts] = unique(BeadBarcodes, 'stable');
[~, b] = ismember( BeadBarcodes , BeadBarcodes( BBFirstRef( accumarray(BBOccCounts,1) > 1 ) ) );
UniqueBeadBarcodes2 = BeadBarcodes( b < 1 );
UniqueBeadLocations = BeadLocations( b < 1 );
BaseBalanceBarcodes = [UniqueBeadBarcodes2];
BaseBalanceBase5Barcodes = cellfun( @(x) reverse(string(x)) , {dec2base(BaseBalanceBarcodes,5,NumBases)} , 'UniformOutput' , false);
BaseBalanceBase5Barcodes = BaseBalanceBase5Barcodes{1};
UniqueBeadBarcodesForExport = char( replace( BaseBalanceBase5Barcodes , {'0','1','2','3','4'} , {'N','T','G','C','A'} ) );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FHB = fopen( fullfile(OutDir, [Puck, '_barcodes.unsorted.txt']) , 'w' );

FHL = fopen( fullfile(OutDir, [Puck, '_locations.unsorted.csv']) , 'w' );
fprintf(FHL, 'Barcode,x,y\n');

for i = 1:length(UniqueBeadBarcodesForExport)

	sequence = UniqueBeadBarcodesForExport(i,:);
	bead = UniqueBeadLocations(i);
	row = sprintf('%s,%.2f,%.2f\n', sequence, bead{1}(1), bead{1}(2));

	fprintf(FHB, [sequence, '\n']);
	fprintf(FHL, row);

end

fclose(FHB);
fclose(FHL);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('Bye');
quit(0)

end
