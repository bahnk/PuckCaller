
process split_channels {

	tag { "${name}" }
   
	label "libtiff"

	executor "slurm"
	cpus 2
	time "00:30:00"
	maxForks 4

	publishDir { "pucks/split_channels/${puck_label}" }, mode: "copy", overwrite: true

	input:
		tuple val(metadata), path(tif), path(script)

	output:
		tuple val(metadata), path("${name}_channel*.tif")

	script:		
		
      name = sprintf("%s_%s_%s_%s",
               metadata["puck_label"],
               metadata["base_label"],
               metadata["ligation_label"],
               metadata["primer_label"]
               )

		puck_label = metadata["puck_label"]

		"""
      python3 $script $tif $name
		"""
}

process z_select {

	tag { "${name}" }
   
	label "libtiff"

	executor "slurm"
	cpus 2
	time "00:30:00"
	maxForks 4

	publishDir { "pucks/z_selection/${puck_label}" }, mode: "copy", overwrite: true

	input:
		tuple val(metadata), path(tifs), path(script)

	output:
		tuple val(metadata), path("${name}.tif"), emit: tif
		tuple val(metadata), path("${name}.csv"), emit: csv

	script:		
		
      name = sprintf("%s_%s_%s_%s_zselect",
               metadata["puck_label"],
               metadata["base_label"],
               metadata["ligation_label"],
               metadata["primer_label"]
               )

      puck = metadata["puck"]
      ligation = metadata["ligation"]

		puck_label = metadata["puck_label"]

		"""
      python3 $script $name $puck $ligation $tifs
		"""
}

