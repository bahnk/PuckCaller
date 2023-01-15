
process report {

	label "python"

	executor "slurm"

	time "00:30:00"

	publishDir path: { "pucks" }, mode: "copy", overwrite: true,
		saveAs: {
			filename ->
			if ( filename.indexOf("Run") != -1 ) {
				"${filename}"
			} else {
				"results/${filename}"
			}
		}

	input:
		tuple path(files), path(script)

	output:
		path "Run${date}_overview.png", emit: overview
		path "Run${date}_metrics.csv", emit: metrics
		path "Run${date}_zselection.pdf", emit: zselection
		path "*_locations.csv", emit: locations
		path "*_barcodes.txt", emit: barcodes

	script:		
		
		date = params.date
		slices = params.slices

		"""
		python3 $script $date $slices . .
		"""
}

