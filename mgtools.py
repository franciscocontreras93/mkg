# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mgtools
                                 A QGIS plugin
 Conjunto de Herramientas para el Procesado de Información Geoestadisitica 
                              -------------------
        begin                : 2021-03-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Francisco Contreras, GeoSIG
        email                : FranciscoContreras93@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# pyqgis and pyqt5 libraries
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction, QInputDialog
from qgis.utils import *
from qgis.core import * 
from qgis.core import QgsProject 
from PyQt5 import QtWidgets, QtCore
# python libraries
import os
import pandas as pd
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .dialogs import transformDialog, exportDialog, classDialog
# plugin libraries
#_________________#


icons_path = {
    'transformar': r'gui\icon\transform_black_24dp.svg',
    'exportar': r'gui\icon\file_upload_black_24dp.svg',
    'filtrar': r'gui\icon\filter_alt_black_24dp.svg',
    'open': r'gui\icon\launch_black_24dp.svg',
    'update': r'gui\icon\explore_black_24dp.svg',
}

# TODO: 

#properties = {
# 'name': 'circle', 
# 'color': '#0000ff', 
# 'outline_style': 'no', 
# 'size': size
# }

#symbol = QgsMarkerSymbol.createSimple(properties)

#######

class mgtools:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.project = QgsProject.instance()
        self.layerTreeRoot = self.project.layerTreeRoot()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'mgtools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Herramientas Marketing Group')
        self.mg_menu = QtWidgets.QMenu(self.tr(u'&MG Herramientas'))
        self.toolbar =  self.iface.addToolBar(u'Herramientas MG')
        self.tdaLine = QtWidgets.QLineEdit()
        self.tdaLine.setFixedWidth(80)
        self.tdaLine.setPlaceholderText("Cod. Tienda")
        self.tdaLabel = QtWidgets.QLabel()
        self.tdaLabel.setText('Filtrar Tienda: ')
        self.tdaLabel.setStyleSheet("font-weight: bold;")



        

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('mgtools', message)
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=False,
        add_to_toolbar=False,
        status_tip=None,
        whats_this=None,
        shortcut = None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        
        if shortcut is not None:
            action.setShortcut(shortcut)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action
    def iconPath(self,icon):
        _icon = os.path.join(self.plugin_dir, icons_path[f"{icon}"])
        return _icon
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/mgtools/icon.png'
        transform_path = ':/plugins/mgtools/gui/icon/transform_black_24dp.svg'
        export_path = ':/plugins/mgtools/gui/icon/file_upload_black_24dp.svg'
        filter_path = ':/plugins/mgtools/gui/icon/filter_alt_black_24dp.svg'
        style_path = ':/plugins/mgtools/gui/icon/style_black_24dp.svg'
        update_path = ':/plugins/mgtools/gui/icon/explore_black_24dp.svg'
        search_path = ':/plugins/mgtools/gui/icon/search_black_24dp.svg'

        transformar = self.add_action(transform_path, text=self.tr(
            u'Transformar a CSV'), add_to_toolbar=True, callback=self.addCsvToMap, parent=self.iface.mainWindow())
        
        transformar.setShortcut('CTRL+7')
        
        exportar = self.add_action(export_path,text=self.tr(
            u'Exportar a CSV'), add_to_toolbar=True, callback=self.export_run, parent=self.iface.mainWindow())
        estilo = self.add_action(style_path, text=self.tr(
            u'Filtrar Tienda'), add_to_toolbar=True, callback=self.class_run, parent=self.iface.mainWindow())
        coordenadas = self.add_action(update_path, text=self.tr(
            u'Actualizar Coordenadas'), add_to_toolbar=True, callback=self.updateCoordinates, parent=self.iface.mainWindow())

        #open_file = self.add_action(open_path, text=self.tr(
        #    u'Abrir Proyecto'), add_to_toolbar=True, callback=self.openProject, parent=self.iface.#mainWindow())
        self.toolbar.addWidget(self.tdaLabel)
        self.toolbar.addWidget(self.tdaLine)

        search = self.add_action(search_path, text=self.tr(
            u'Filtrar Tienda'), add_to_toolbar=True, callback=self.searchTda, parent=self.iface.mainWindow())

        # will be set False in run()
        #self.mg_menu.addAction(transformar)
        #self.mg_menu.addAction(exportar)
        #self.mg_menu.addAction(filtrar)
        #self.iface.mainWindow().menuBar().insertMenu(action,self.mg_menu) # AGREGAR MENU A LA BARRA DE MENUS
        #self.first_start = True
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Herramientas Marketing Group'),
                action)
            self.iface.removeToolBarIcon(action)
    
    def export_run(self):
        layers = QgsProject.instance().mapLayers().values()
        vectorlayers = [layer for layer in layers if layer.type()
                      == QgsMapLayer.VectorLayer]
        self.dlg = exportDialog()
        self.dlg.lineEdit.clear()      
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            self.exportar()
            pass      
    def filter_run(self):        
        self.filterDlg = filterDialog()       
        self.filterDlg.show()
        #tda_check = self.filterDlg.tda.isChecked()
        #folleto_check = self.filterDlg.folleto.isChecked()        
        self.filterDlg.pushButton.clicked.connect(self.check) 
    def class_run(self):
        self.classDlg = classDialog()
        self.classDlg.show()
        
        self.classDlg.pushButton.clicked.connect(self.p14_class)

#----------------------------------------------------------------------#  

    
    def exportar(self):
        os.chdir(self.dlg.lineEdit.text())
        file_name = self.dlg.lineEdit_2.text()
        group = self.layerTreeRoot.findGroup("BASES")

        total = 0

        if group:
            try:
                layers = group.findLayers()
                for layer in layers:
                    total += 1
                    layerName = layer.name()
                    vLayer = self.project.mapLayersByName(layerName)[0]
                    QgsVectorFileWriter.writeAsVectorFormat(vLayer, f"{layerName}.csv", "utf-8",
                                                            vLayer.crs(), "CSV")
                iface.messageBar().pushMessage("Resultado:", f"Exportado Correctamente {total} Capas", level=3)
            
            except:
                pass

        try:
            extension = 'csv'
            total = 0
            all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
            for e in all_filenames:
                total += 1
            combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
            combined_csv.to_csv(f"{file_name}.csv", index=False, encoding='utf-8')
            iface.messageBar().pushMessage(
                "Resultado:", f"Se combinaron un total de {total} elementos", level=3)
        except:
            pass











        # self.layer2Export = QgsProject.instance().mapLayersByName(self.layerName)[0]
        # iface.setActiveLayer(self.layer2Export)
        # self.layer = iface.activeLayer()
        # self.path2csv = self.dlg.lineEdit.text()
        # QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.path2csv, "utf-8", QgsCoordinateReferenceSystem(), "CSV")
        # #self.tools.export_as_csv(self.layer, self.path2csv)
        # iface.messageBar().pushMessage("Resultado:", f"Exportado Correctamente {self.layerName}", level=3)
    def searchTda(self):
        
        try:
           
            tiendaId = int(self.tdaLine.text())
            exp = f""""ID MG" ={tiendaId}"""
            exp2 = f""""5km" LIKE '%{tiendaId}%' AND "graficar" = 'SI'"""
            QgsExpressionContextUtils.setProjectVariable(self.project, 'id_tda', tiendaId)
            tdaLayer = self.project.mapLayersByName("tda ched")[0]
            cmpLayer = self.project.mapLayersByName("COMPETIDORES 2KM")[0]
            tdaLayer.setSubsetString(exp)
            cmpLayer.setSubsetString(exp2)
            iface.setActiveLayer(tdaLayer)  # activar capa
            iface.zoomToActiveLayer()  # zoom a capa activa
            tdaLayer.setSubsetString("")
            
            self.canvas.zoomScale(35000)

        except: 
            self.iface.messageBar().pushMessage("Error:", "Debe Ingresar una Tienda ", level=2)
    def addCsvToMap(self):
        answer = QInputDialog().getText(None, "Información:", "Ingresa el nombre del archivo CSV")
        fileName = answer[0]
        pathToCsv = f'C:/ISMAEL/entregas/{fileName}.csv'
        GpName = r'C:/ISMAEL/2021 FOLLETO.gpkg'
        xField = 'longitud'
        yField = 'latitud'
        uri = f"file:///{pathToCsv}?encoding=utf-8&type=csv&maxFields=10000&detectTypes=yes&decimalPoint=,&xField={xField}&yField={yField}&crs=EPSG:4686&spatialIndex=no&subsetIndex=no&watchFile=yes"
        csv_layer = QgsVectorLayer(uri, fileName, 'delimitedtext')
        layer = csv_layer

        done = 'Proceso Exitoso'
        error = 'Error'

        #QgsProject.instance().addMapLayer(csv_layer)
        #iface.setActiveLayer(csv_layer)
        #layer = iface.activeLayer()



        
        # agregar capa csv geografica a geopackage
        if layer.isValid():
            try:
                options = QgsVectorFileWriter.SaveVectorOptions()
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer  # Update mode
                options.EditionCapability = QgsVectorFileWriter.CanAddNewLayer
                options.layerName = layer.name()

                _writer = QgsVectorFileWriter.writeAsVectorFormat(
                    layer, GpName, options)
                if _writer[0] == QgsVectorFileWriter.ErrCreateDataSource:
                    #print("Create mode")
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile  # Create mode
                    _writer = QgsVectorFileWriter.writeAsVectorFormat(
                        layer, GpName, options)
                print(done)
            except:
                print(error)
        # llamada a capa desde el geopackage al mapa
        try:

            layer_gpkg = GpName + f'|layername={fileName}'
            layer = QgsVectorLayer(layer_gpkg, fileName, 'ogr')
            if not layer.isValid():
                print('Error de Capa')
            else:
                QgsProject.instance().addMapLayer(layer)
        except:
            print('Algo Salio Mal')   
    def updateCoordinates(self):
        # imports
        # accessing point layer by name
        # layer = QgsProject.instance().mapLayersByName('1180-TEPOZAN_OKI')[0]
        layer = iface.activeLayer()
        latNameField = ""
        longNameField = ""

        try:
            if not layer.isValid():
                self.iface.messageBar().pushMessage("",
                                                    f"La capa no es Valida", level=2)
            layer_provider = layer.dataProvider()
            # adding new fields
            # for attr in ["X_Coord", "Y_Coord"]:
            #   layer_provider.addAttributes([QgsField(attr, QVariant.Double)])
            # layer.updateFields()
            fields = layer.fields()  # accessing layer fields
            for field in fields:
                if field.name() == "latitud":
                    latNameField = "latitud"
                elif field.name()=="longitud":
                    longNameField = "longitud"
                elif field.name() == "LATITUD":
                    latNameField = "LATITUD"
                elif field.name() == "LONGITUD":
                    longNameField = "LONGITUD"

            # starting layer editing
            if not layer.isEditable():
                layer.startEditing()

            for feature in layer.getFeatures():

                attrs = {
                    fields.indexFromName(longNameField): feature.geometry().asPoint().x(),
                    fields.indexFromName(latNameField): feature.geometry().asPoint().y()
                }
                layer_provider.changeAttributeValues({feature.id(): attrs})
                
            
            layer.commitChanges() # guardar cambios en la capa            
            self.iface.messageBar().pushMessage("",
                                                f"Coordenadas Actualizadas {layer}", level=3)
        except:
            self.iface.messageBar().pushMessage("",
                                                f"Ocurrio un error", level=2)
    def p14_class(self):
        layer = iface.activeLayer()
        # print(layer.name())
        tdaLayer = self.project.mapLayersByName("tda ched")[0]
        cmpLayer = self.project.mapLayersByName("COMPETIDORES 2KM")[0]
        valor = self.classDlg.lineEdit.text()
        arr = valor.split(";")

        if layer.name() == tdaLayer.name() or layer.name() == cmpLayer.name():
        
           self.mensajes("error","SELECCIONA OTRA CAPA",2)
           pass
        else:       
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            renderer = QgsRuleBasedRenderer(symbol)
            
            root_rule = renderer.rootRule()        
            else_rule = root_rule.children()[0]
            else_rule.setFilterExpression('ELSE')
            #else_rule.symbol().setColor(QColor('black'))
            

            for e in arr:
                expresion = f'"p14_1" = {e} or "p14_2" = {e} or "p14_3" = {e}'
                rule = root_rule.children()[0].clone()
                rule.setFilterExpression(expresion)
                
                root_rule.appendChild(rule)

            layer.setRenderer(renderer)
            layer.triggerRepaint()
            iface.layerTreeView().refreshLayerSymbology(layer.id())
            pass
    def mensajes(self,title,cadena,lvl):
        iface.messageBar().pushMessage(title,cadena, level = lvl)
        pass
#----------------------------------------------------------------------#
# QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),'myvar','AJUSCO')
