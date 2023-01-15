
process puckcaller {
	tag { "${puck}" }

	label "matlab"

	executor "slurm"
	time "03:00:00"
	memory "100G"
	cpus 12

	maxForks 1

	publishDir { "pucks/${puck}" }, mode: "copy", overwrite: true,
		saveAs: {

			filename ->

			if ( filename.indexOf(".mat") != -1 ) {
				"MATLAB_Objets/${filename}"
			}

			else if ( filename.indexOf("${puck}_indices.tif") != -1 ) {
				"${filename}"
			}

			else if ( filename.indexOf(".tif") != -1 ) {

				if ( filename.indexOf("_image.tif") != -1 ) {
					"${filename}"
				}

				else {
					def type = filename.replaceAll(".*_(\\w+).tif", "\$1")
					"${type}/${filename}"
				}
			}

			else if ( filename.indexOf("_transform.csv") != -1 ) {
				"transform_csv/${filename}"
			}

			else {
				"${filename}"
			}
		}

	input:
		tuple val(puck), file(tifs), val(script)

	output:
		tuple val(puck), file("*_adjust.mat"), emit: adjust_mat
		tuple val(puck), file("*_balanced.mat"), emit: balanced_mat
		tuple val(puck), file("*_indices.mat"), emit: indices_mat
		tuple val(puck), file("*_mixing.mat"), emit: mixing_mat
		tuple val(puck), file("*_tophat.mat"), emit: tophat_mat
		tuple val(puck), file("*_transform.mat"), emit: transform_mat
		tuple val(puck), file("*_offset.tif"), emit: offset_tif
		tuple val(puck), file("*_adjust.tif"), emit: adjust_tif
		tuple val(puck), file("*_balanced.tif"), emit: balanced_tif
		tuple val(puck), file("*_indices.tif"), emit: indices_tif
		tuple val(puck), file("*_mixing.tif"), emit: mixing_tif
		tuple val(puck), file("*_tophat.tif"), emit: tophat_tif
		tuple val(puck), file("*_transform.tif"), emit: transform_tif
		tuple val(puck), file("*_transform.csv"), emit: transforms
		tuple val(puck), file("*_offsets.csv"), emit: offsets
		tuple val(puck), file("*_multipliers.csv"), emit: multipliers
		tuple val(puck), file("*_barcodes.unsorted.txt"), emit: barcodes
		tuple val(puck), file("*_locations.unsorted.csv"), emit: locations
		tuple val(puck), file("*_image.tif"), emit: image

	script:		
		"""
		mkdir mcr_cache_root
		export MCR_CACHE_ROOT=\$PWD/mcr_cache_root
		echo \$MCR_CACHE_ROOT
		eval "\\"${script}\\"" ./ ./ $task.cpus
		"""
}

