# Marketing Group Plugin

Complemento desarrollado por GeoSIG Consultoria. Para uso interno del proyecto Ofrecido a MarketingGroup Mexico. 

Posee varias herramientas necesarias para el optimo desarrollo de las actividades contratadas.

## Why?

For educational purposes, it is useful to understand how a very basic plugin could look like.

For practical reasons, it is sometimes useful to create a single purpose plugin with the least amount of extra bells and whistles,
so the code that actually does something is not hidden among generated boilerplate code.

## How to use it?

1. Create a new python plugin directory
  * e.g. Linux ```~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/minimal```
  * e.g. Windows ```C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\minimal```
2. Copy ```metadata.txt``` and ```__init__.py``` to that directory
3. Start QGIS and enable the plugin (menu Plugins > Manager and Install Plugins...)

Now you should see a "Go!" button in your "Plugins" toolbar (make sure it is enabled in menu Settings > Toolbars > Plugins).

The next step is to change the metadata (e.g. plugin title and description) in ```metadata.txt``` and
start adding your own code to ```__init__.py```. Have fun!
