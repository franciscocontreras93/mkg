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
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import *
from qgis.core import * 
from qgis.core import QgsProject 
from PyQt5 import QtWidgets
# python libraries
import os.path
import pandas as pd
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .dialogs import transformDialog, exportDialog, filterDialog, classDialog
# plugin libraries
#_________________#


icons_path = {
    'transformar': r'gui\icon\transform_black_24dp.svg',
    'exportar': r'gui\icon\file_upload_black_24dp.svg',
    'filtrar': r'gui\icon\filter_alt_black_24dp.svg',
    'open': r'gui\icon\launch_black_24dp.svg',
    'update': r'gui\icon\explore_black_24dp.svg',
}

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
        #action = self.add_action(icon_path,
        #    text=self.tr(u'MG Herramientas'),
        #    callback=self.transform_run,
        #    parent=self.iface.mainWindow())

        transform_path = ':/plugins/mgtools/gui/icon/transform_black_24dp.svg'
        export_path = ':/plugins/mgtools/gui/icon/file_upload_black_24dp.svg'
        filter_path = ':/plugins/mgtools/gui/icon/filter_alt_black_24dp.svg'
        style_path = ':/plugins/mgtools/gui/icon/style_black_24dp.svg'
        update_path = ':/plugins/mgtools/gui/icon/explore_black_24dp.svg'

        transformar = self.add_action(transform_path, text=self.tr(
            u'Transformar a CSV'), add_to_toolbar=True, callback=self.transform_run, parent=self.iface.mainWindow())
        
        transformar.setShortcut('CTRL+7')
        
        exportar = self.add_action(export_path,text=self.tr(
            u'Exportar a CSV'), add_to_toolbar=True, callback=self.export_run, parent=self.iface.mainWindow())
        
        filtrar = self.add_action(filter_path, text=self.tr(
            u'Filtrar Tienda'), add_to_toolbar=True, callback=self.filter_run, parent=self.iface.mainWindow())
        estilo = self.add_action(style_path, text=self.tr(
            u'Filtrar Tienda'), add_to_toolbar=True, callback=self.class_run, parent=self.iface.mainWindow())
        coordenadas = self.add_action(update_path, text=self.tr(
            u'Actualizar Coordenadas'), add_to_toolbar=True, callback=self.updateCoordinates, parent=self.iface.mainWindow())

        #open_file = self.add_action(open_path, text=self.tr(
        #    u'Abrir Proyecto'), add_to_toolbar=True, callback=self.openProject, parent=self.iface.#mainWindow())

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
    def transform_run(self):        
        self.transformDialog = transformDialog()
        self.transformDialog.show()
        
        #if self.transformDialog.lineEdit.textChanged():
        #    print("algo")

        result = self.transformDialog.exec_()
        if result:
            if self.transformDialog.lineEdit.text():
                self.transformar()
            else:
                self.iface.messageBar().pushMessage(
                    "Resultado:", "Debe seleccionar un Archivo ", level=2)

            
                
         
           
            
            pass
    def export_run(self):
        layers = QgsProject.instance().mapLayers().values()
        vectorlayers = [layer for layer in layers if layer.type()
                      == QgsMapLayer.VectorLayer]
        self.dlg = exportDialog()
        self.dlg.comboBox.clear()
        self.dlg.lineEdit.clear()
        self.dlg.comboBox.addItems([layer.name() for layer in vectorlayers])
        
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
    def readExcel(self,file_path):

        file_path = file_path
        read_file = pd.read_excel(file_path, engine="openpyxl")

        return read_file
    def fillComboLatLong(self, file_path):
        read_file = self.readExcel(file_path)


        e = 0
        headers = []
           # PRUEBA HEADERS #
        for i in read_file.columns:
            headers.append(i)
            e += 1
            if e >= 18:
                break
        for h in headers:
            #self.transformDialog.comboLat.addItems(h)
            pass
        print(len(headers))
    def transformar(self):
        try: 
            file_path = self.transformDialog.lineEdit.text()
            read_file = self.readExcel(file_path)
            #self.fillComboLatLong(file_path)
            #-----------------------#
            _path = os.path.abspath(file_path)
            output_path = os.path.dirname(_path)
            _file_name = os.path.basename(_path)[:-5]
            read_file.to_csv(f"{output_path}/{_file_name}.csv",index=None, header=True)
            #latitud = self.transformDialog.latitud.text()
            #longitud = self.transformDialog.longitud.text()
            self.iface.messageBar().pushMessage("Resultado:",
                                                f"Transformación Exitosa del archivo <a href='{output_path}'>{_file_name}</a>", level=3)
            #self.addCsvToMap(file_path, latitud, longitud)
        except:
            self.iface.messageBar().pushMessage("Resultado:", "Error en la Ejecución ", level=2)
    def exportar(self):
        self.layerName = str(self.dlg.comboBox.currentText())
        self.layer2Export = QgsProject.instance().mapLayersByName(self.layerName)[0]
        iface.setActiveLayer(self.layer2Export)
        self.layer = iface.activeLayer()
        self.path2csv = self.dlg.lineEdit.text()
        QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.path2csv, "utf-8", QgsCoordinateReferenceSystem(), "CSV")
        #self.tools.export_as_csv(self.layer, self.path2csv)
        iface.messageBar().pushMessage("Resultado:", f"Exportado Correctamente {self.layerName}", level=3)
    def filtrarTda(self):
        try:
            tiendaId = int(self.filterDlg.lineEdit.text())
            exp = f'"ID MG"={tiendaId}'      
            iconLayer = QgsProject.instance().mapLayersByName("tda ched")[0]
            labelLayer = QgsProject.instance().mapLayersByName("ETIQUETAS")[0]
            iconLayer.setSubsetString(exp)
            labelLayer.setSubsetString(exp)
            iface.setActiveLayer(iconLayer)  # activar capa
            iface.zoomToActiveLayer()  # zoom a capa activa
        except: 
            self.iface.messageBar().pushMessage("Resultado:", "Debe Cargar el Proyecto ", level=2)
    def filtrarFolleto(self):
        try:
            tiendaId = int(self.filterDlg.lineEdit.text())
            exp = f'"ID MG"={tiendaId}'
            iconLayer = QgsProject.instance().mapLayersByName("folleto ched")[0]
            labelLayer = QgsProject.instance().mapLayersByName("ETIQUETAS")[0]
            iconLayer.setSubsetString(exp)
            labelLayer.setSubsetString('')
            iface.setActiveLayer(iconLayer)  # activar capa
            iface.zoomToActiveLayer()  # zoom a capa activa
            iface.mapCanvas().zoomScale(35000.0)
        except:
            self.iface.messageBar().pushMessage(
                "Resultado:", "Debe Cargar el Proyecto", level=2)      
    def check(self):
        if self.filterDlg.tda.isChecked():
            self.filtrarTda()
        elif self.filterDlg.folleto.isChecked():
            self.filtrarFolleto()
        else:
            self.iface.messageBar().pushMessage(
                "Resultado:", "Error en la Ejecución ", level=2)
    def openProject(self):
        #uri = r'F:/FRANCISCO/GIS/ISMAEL/ESTRATEGICO/PROYECTO 2020.qgz'
        #QgsProject.instance().read(uri)
        pass
    def addCsvToMap(self,csv_path,latitud,longitud):
        uri = f'file:///{csv_path}?encoding=UTF-8&delimiter=,&yField={latitud}&xField={longitud}'
        "file:///C:/Users/FRANCISCO/Downloads/Telegram%20Desktop/1055-NEZA%20IMPULSORA_RE_OKI%20(2).csv?encoding=System&type=csv&detectTypes=yes&decimalPoint=,&xField=LONGITTUD&yField=LATITUD&crs=EPSG:4686&spatialIndex=no&subsetIndex=no&watchFile=yes"
        layer = QgsVectorLayer(uri, 'test', 'delimitedtext')
        QgsProject.instance().addMapLayer(layer)
        print(layer.isValid())
    
    def updateCoordinates(self):
        # imports
        # accessing point layer by name
        # layer = QgsProject.instance().mapLayersByName('1180-TEPOZAN_OKI')[0]
        layer = iface.activeLayer()

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

            # starting layer editing
            layer.startEditing()

            for feature in layer.getFeatures():
                attrs = {
                    fields.indexFromName("LONGITUD"): feature.geometry().asPoint().x(),
                    fields.indexFromName("LATITUD"): feature.geometry().asPoint().y()
                }
                layer_provider.changeAttributeValues({feature.id(): attrs})

            layer.commitChanges()
            self.iface.messageBar().pushMessage("",
                                                f"Coordenadas Actualizadas {layer}", level=3)
        except:
            self.iface.messageBar().pushMessage("",
                                                f"Ocurrio un error", level=2)





    def p14_class(self):
        layer = iface.activeLayer()
        valor = self.classDlg.lineEdit.text()
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        renderer = QgsRuleBasedRenderer(symbol)
        expresion = f'"p14_1" = {valor} or "p14_2" = {valor} or "p14_3" = {valor}'
        root_rule = renderer.rootRule()        
        else_rule = root_rule.children()[0]
        else_rule.setFilterExpression('ELSE')
        #else_rule.symbol().setColor(QColor('black'))

        rule = root_rule.children()[0].clone()
        rule.setFilterExpression(expresion)
        if valor == 42:
            rule.setLabel('Waltmart')
            rule.symbol().setColor(QColor('blue'))
        elif valor == 4:
            rule.setLabel('Aurrera')
            rule.symbol().setColor(QColor('green'))
        elif valor == 12:
            rule.setLabel('Chedraui')
            rule.symbol().setColor(QColor('orange'))

        root_rule.appendChild(rule)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(layer.id())
        
        pass
#----------------------------------------------------------------------#
