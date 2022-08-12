#!/usr/bin/env wolframscript
(* ::Package:: *)

f = OpenRead["C:\\Users\\jakob\\Documents\\GitHub\\wordle_bot\\data\\allowed.txt"];
data = ReadList[f, String];
Close[f];

f = OpenWrite["C:\\Users\\jakob\\Documents\\GitHub\\wordle_bot\\data\\frequencies_wolfram.txt"];

For[i = 1, i <= Length[data], i++,
  Write[f, WordFrequencyData[data[[i]]]]
];

Close[f];
Print["done!"]
