# Integration Capacity Analysis (ICA)

This OpenFIDO pipeline perform Integration Capacity Analysis (ICA) on an arbitrary GridLAB-D model.  The model must satisfy the following prerequisite conditions:

1) use the GridLAB-D `powerflow` module
2) include a working distribution system network using `powerflow` module object such as `line`, `transformer`, etc. with ratings or limits specified.
3) include `load` objects
