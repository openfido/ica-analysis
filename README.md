# Integration Capacity Analysis (ICA)

This OpenFIDO pipeline perform Integration Capacity Analysis (ICA) on an arbitrary GridLAB-D model.  The model must satisfy the following prerequisite conditions:

1) use the GridLAB-D `powerflow` module
| 2) include a working distribution system network using `powerflow` module object such as `line`, `transformer` |  etc. with ratings or limits specified. |
3) include `load` objects

# Example

The following runs the ICA analysis from the command line using the ICA files in the `autotest/input_1` folder:

~~~
shell% gridlabd config.glm IEEE-13.glm ica_analysis.glm
~~~

It generates the `solar_capacities.csv` file:

~~~
| load | solar_capacity[kW] |
| ---- | ------------------ |
| Load634 | 840.0 |
| Load645 | 1140.0 |
| Load646 | 9420.0 |
| Load652 | 2570.0 |
| Load671 | 2640.0 |
| Load675 | 1680.0 |
| Load692 | 8340.0 |
| Load611 | 1320.0 |
| Load6711 | 2760.0 |
| Load6321 | 4200.0 |
~~~
