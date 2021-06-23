This system uses NumPy for its logi and wxPython for its UI.

Elements:

pipeline and context handle the general data state and the execution order. 
A pipeline is composed of mapOps.AbstractSidebar objects. All map operations must inherit from that type.
The ui module contains the definition of the host Frame and handles the general events. It also contains the UI Elements that are Sidebar independent.
The MapOps module describes all transformation steps on the dataset.