#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPaletteProtocol = objc.protocolNamed( "GlyphsPalette" )

class SmilyPalette ( NSObject, GlyphsPaletteProtocol ):
	
	_theView = objc.IBOutlet()
	_theImageView = objc.IBOutlet()
	def init( self ):
		"""
		Do all initializing here.
		"""
		
		if not NSBundle.loadNibNamed_owner_("SmilyPaletteView", self):
			self.logToConsole("Palette.Layers: Error loading Nib!")
		
		s = objc.selector( self.update, signature='v@:' )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentCloseNotification", None )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentActivateNotification", None )
		
		Frame = self._theView.frame()
		
		if NSUserDefaults.standardUserDefaults().objectForKey_( "com.GeorgSeifert.SmilyPalette.ViewHeight" ):
			Frame.size.height = NSUserDefaults.standardUserDefaults().integerForKey_( "com.GeorgSeifert.SmilyPalette.ViewHeight" )
			self._theView.setFrame_(Frame)
		
		#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
		return self
		
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		return "Smily"
	
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		return 1
	
	def theView( self ):
		"""
		return a NSView to be displayed in the palette.
		"""
		print "__self.theView", self.theView
		return self._theView
	
	def minHeight( self ):
		"""
		the minimal size of the view
		"""
		return 78
	
	def maxHeight( self ):
		"""
		the maximal size of the view.
		has to be equal or bigger than minHeight
		"""
		return 78
	
	def currentHeight( self ):
		"""
		the current height. Used for storing the current resized state.
		"""
		return 78 #NSUserDefaults.standardUserDefaults().integerForKey_( "com.GeorgSeifert.SmilyPalette.ViewHeight" )
	
	def setCurrentHeight_( self, newHeight ):
		if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
			NSUserDefaults.standardUserDefaults().setInteger_forKey_( newHeight, "com.GeorgSeifert.SmilyPalette.ViewHeight" )
	
	def currentWindowController( self, sender ):
		windowController = None
		try:
			windowController = NSDocumentController.sharedDocumentController().currentDocument().windowController()
			if not windowController and sender.respondsToSelector_("object"):
				if sender.object().__class__ == NSClassFromString("GSFont"):
					Font = sender.object()
					windowController = Font.parent().windowControllers()[0]
					self.logToConsole("__windowController1", windowController)
				else:
					windowController = sender.object()
					self.logToConsole( "__windowController2", windowController )
		except:
			pass
		return windowController
	
	def update( self, sender ):
		"""
		is called from the notificationCenter if the info in the current Glyph window has changed. This might be called quite a lot, so keep the method fast.
		"""
		Layer = None
		try:
			windowController = self.currentWindowController(sender)
			Layer = windowController.activeLayer()
		except:
			pass
		if Layer:
			self._theImageView.setHidden_(False)
		else:
			self._theImageView.setHidden_(True)
			
		
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
	