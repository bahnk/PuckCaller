#!/usr/bin/env nextflow

nextflow.enable.dsl=2

import java.nio.file.Paths

@Grab('com.xlson.groovycsv:groovycsv:1.3')
import static com.xlson.groovycsv.CsvParser.parseCsv

///////////////////////////////////////////////////////////////////////////////
//// METHODS //////////////////////////////////////////////////////////////////

///////////////////////////
def dropKeys(map, keys) {//
///////////////////////////
	// because Map.dropWhile doesn't with the current Java version of Nextflow,
	// apparently requires Java9
	def new_map = [:]
	map.each{ k, v ->
		if ( ! keys.contains(k) ) {
			new_map[k] = v
		}
	}
	return new_map
}

///////////////////////
def mergeMaps(item) {//
///////////////////////

	def new_map = [:]
	def map1 = item[1].clone()
	def map2 = item[3].clone()

	map1.each{ k, v -> new_map[k] = v }
	map2.each{ k, v -> new_map[k] = v }


	return [ new_map , item[4] ]
}

////////////////////////////////
def getInfoFromTif(filename) {//
////////////////////////////////

	def regex = "220609_ligation_(\\d+)_MMStack_Pos(\\d+).ome.tif"

	def ligation = filename.replaceAll(regex, "\$1")
	def position = filename.replaceAll(regex, "\$2")

	def m = [:]

	m["date"] = params.date

	m["ligation"] = ligation
	m["ligation_label"] = "ligation" + ligation.toString().padLeft(2, "0")

	m["position"] = position
	m["position_label"] = "position" + position.toString().padLeft(2, "0")

	m["puck"] = Integer.parseInt(position).toString()
	m["puck_label"] =
		"puck" + Integer.parseInt(position).toString().padLeft(2, "0")

	primer_map = [
		"T-1": "Tminus1",
		"T": "T",
		"T+1": "Tplus1",
		"T+2": "Tplus2",
		"T+3": "Tplus3",
		"3UP+1": "3UPplus1",
		"3UP": "3UP",
		"3UP-1": "3UPminus1",
		"UP-1": "UPminus1",
		"UP": "UP",
		"UP+1": "UPplus1",
		"UP+2": "UPplus2",
		"UP+3": "UPplus3",
		"UP+4": "UPplus4"
	]

	order = parseCsv( new File(params.order).getText() )

	for (row in order) {

		if ( ligation == row.ligation ) {

			m["base"] = row.base
			m["base_label"] = "base" + row.base.toString().padLeft(2, "0")

			m["primer"] = row.primer
			m["primer_label"] = primer_map[row.primer]
		}
	}

	return m
}

///////////////////////////////////////////////////////////////////////////////
//// BINARIES /////////////////////////////////////////////////////////////////

split_channels_bin = Channel.fromPath("./bin/split_channels.py")
z_select_bin = Channel.fromPath("./bin/z_select.py")
puckcaller_bin = Channel.fromPath("./bin/PuckCaller/bin/PuckCaller")
report_bin = Channel.fromPath("./bin/report.py")

///////////////////////////////////////////////////////////////////////////////
//// PROCESSES ////////////////////////////////////////////////////////////////

include { split_channels } from "./modules/process/preprocess"
include { z_select } from "./modules/process/preprocess"

include { puckcaller } from "./modules/process/calling"

include { report } from "./modules/process/quality_control"

///////////////////////////////////////////////////////////////////////////////
//// INPUT ////////////////////////////////////////////////////////////////////

regex = "220609_ligation*_MMStack_Pos*.ome.tif"

Channel
	.fromPath( Paths.get(params.directory, regex ) )
	.map{[ getInfoFromTif(it.getFileName().toString()) , it ]}
	.filter{ it[0]["puck"] != "19" }
	//.filter{ it[0]["puck"] == "22" }
	//.filter{
	//	it[0]["puck"] == "0" || 
	//	it[0]["puck"] == "10"
	// }
	.set{ TIFFS }

///////////////////////////////////////////////////////////////////////////////
//// MAIN WORKFLOW ////////////////////////////////////////////////////////////

workflow {

	///////////////////////////////////////////////////////////////////////////
	// z selection ////////////////////////////////////////////////////////////

	split_channels( TIFFS.combine(split_channels_bin) )

	split_channels
		.out
		.map{ [ it[0] , it[1].sort{ f -> f.getFileName() } ] }
		.set{ TO_Z_SELECT }

	z_select( TO_Z_SELECT.combine(z_select_bin) )

	///////////////////////////////////////////////////////////////////////////
	// calling ////////////////////////////////////////////////////////////////

	z_select
		.out
		.tif
		.map{ [ it[0]["puck_label"] , it[1] ] }
		.groupTuple()
		.set{ TO_CALL }

	puckcaller( TO_CALL.combine(puckcaller_bin) )

	puckcaller
		.out
		.transforms
		.map{it[1]}
		.concat(
			puckcaller.out.offsets.map{it[1]},
			puckcaller.out.multipliers.map{it[1]},
			puckcaller.out.barcodes.map{it[1]},
			puckcaller.out.locations.map{it[1]},
			puckcaller.out.image.map{it[1]},
			z_select.out.csv.map{it[1]}
		)
		.collect()
		.set{ TO_REPORT }

	report(
		TO_REPORT
			.combine(report_bin)
			.map{ [ it[0..(it.size()-2)] , it[it.size()-1] ] }
	)
}

