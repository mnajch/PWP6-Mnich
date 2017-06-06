import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# MateuszMnichModule
#

class MateuszMnichModule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "MateuszMnichModule" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mateusz Mnich"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# MateuszMnichModuleWidget
#

class MateuszMnichModuleWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)



    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Modele"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Zaladowanie modelu
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = True
    self.inputSelector.noneEnabled = True
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Wybierz model sceny" )
    parametersFormLayout.addRow("Wybrany model: ", self.inputSelector)

    #
    # Suwak dla przezroczystosci
    #
    self.imageOpacitySliderWidget = ctk.ctkSliderWidget()
    self.imageOpacitySliderWidget.singleStep = 1
    self.imageOpacitySliderWidget.minimum = 0
    self.imageOpacitySliderWidget.maximum = 100
    self.imageOpacitySliderWidget.value = 0 # docelowo
    self.imageOpacitySliderWidget.setToolTip( "Wybierz poziom przezroczystosci dla modelu" )
    parametersFormLayout.addRow("Przezroczystosc:", self.imageOpacitySliderWidget)

    #
    # Button dla ukrycia modelu
    #

    self.showOrHideButton = qt.QPushButton()
    self.showOrHideButton.text = "Ukryj lub pokaz"
    self.showOrHideButton.setToolTip("Ukryj lub pokaz model")
    parametersFormLayout.addRow(self.showOrHideButton)

    # connections
    self.showOrHideButton.connect('clicked(bool)', self.onImageVisibilityButton)
    self.imageOpacitySliderWidget.connect('valueChanged(double)', self.onOpacityChanged)

    # Add vertical spacer
    self.layout.addStretch(1)

    # # Refresh Apply button state
    # self.onSelect()

  def cleanup(self):
    pass

  # def onSelect(self):
  #   self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
  #
  # def onApplyButton(self):
  #   logic = MateuszMnichModuleLogic()
  #   logic.showOrHideModel(self.inputSelector.currentNode())

  def onImageVisibilityButton(self):
    logic = MateuszMnichModuleLogic()
    logic.showOrHideModel(self.inputSelector.currentNode())

  def onOpacityChanged(self):
    logic = MateuszMnichModuleLogic()
    opacity = self.imageOpacitySliderWidget.value
    logic.setOpacity(self.inputSelector.currentNode(), opacity)


#
# MateuszMnichModuleLogic
#

class MateuszMnichModuleLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def isValidModelData(self, modelNode):
    """Validates if the model is empty
      """
    if not modelNode:
      logging.debug('isValidAllData failed: no model node defined')
      return False
    return True

  def setOpacity(self, model, opacity):
    if not self.isValidModelData(model):
      slicer.util.errorDisplay('Niewlasciwy model!')
      return False
    n = model.GetDisplayNode()
    n.SetOpacity(opacity/100)
    return True

  def showOrHideModel(self, model):
    if not self.isValidModelData( model):
      slicer.util.errorDisplay('Niewlasciwy model!')
      return False
    n = model.GetDisplayNode()
    v = n.GetVisibility()
    if (v==1):
      n.SetVisibility(0)
    else:
      n.SetVisibility(1)

    # # grab and convert to vtk image data
    # qpixMap = qt.QPixmap().grabWidget(widget)
    # qimage = qpixMap.toImage()
    # imageData = vtk.vtkImageData()
    # slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)
    #
    # annotationLogic = slicer.modules.annotations.logic()
    # annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('MateuszMnichModuleTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class MateuszMnichModuleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_MateuszMnichModule1()

  def test_MateuszMnichModule1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = MateuszMnichModuleLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
