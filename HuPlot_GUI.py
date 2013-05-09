# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wxMatplotlib
import wx.grid

###########################################################################
## Class HuPlot_GUI
###########################################################################

class HuPlot_GUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"HuPlot", pos = wx.DefaultPosition, size = wx.Size( 1000,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 1000,500 ), wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT|wx.NB_TOP )
		self.phd_panel = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.phd_fig = wxMatplotlib.Figure(self.phd_panel, xlabel='Time (ns)', ylabel='Intensity (arb. units)')
		bSizer12.Add( self.phd_fig.canvas, 7, wx.EXPAND, 5 )
		
		self.phd_toolbar = wxMatplotlib.Toolbar( self.phd_fig.canvas )
		bSizer12.Add( self.phd_toolbar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5 )
		
		
		bSizer11.Add( bSizer12, 3, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.phd_checkbox_legend = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Legend@", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.phd_checkbox_legend, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		phd_choice_legend_locChoices = [ u"1", u"2", u"3", u"4", u"5", u"6" ]
		self.phd_choice_legend_loc = wx.Choice( self.phd_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 45,-1 ), phd_choice_legend_locChoices, 0 )
		self.phd_choice_legend_loc.SetSelection( 0 )
		self.phd_choice_legend_loc.SetMaxSize( wx.Size( 45,-1 ) )
		
		bSizer5.Add( self.phd_choice_legend_loc, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer6.Add( bSizer5, 0, 0, 0 )
		
		self.phd_checkbox_normalize = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Normalize", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.phd_checkbox_normalize, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.phd_checkbox_countspersecond = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Counts per second", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.phd_checkbox_countspersecond, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.phd_checkbox_semilog = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Semilog", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.phd_checkbox_semilog, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.phd_checkbox_autoscale_on_drop = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Autoscale on drop", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.phd_checkbox_autoscale_on_drop.SetValue(True) 
		bSizer6.Add( self.phd_checkbox_autoscale_on_drop, 0, wx.LEFT, 5 )
		
		self.phd_checkbox_offset_all = wx.CheckBox( self.phd_panel, wx.ID_ANY, u"Offset all scans same amount", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.phd_checkbox_offset_all.SetValue(True) 
		bSizer6.Add( self.phd_checkbox_offset_all, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.phd_offset_slider = wx.Slider( self.phd_panel, wx.ID_ANY, 0, 0, 13600, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL|wx.SL_INVERSE )
		self.phd_offset_slider.SetToolTipString( u"Adjust offset" )
		
		bSizer6.Add( self.phd_offset_slider, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
		
		self.phd_grid = wx.grid.Grid( self.phd_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.phd_grid.CreateGrid( 0, 3 )
		self.phd_grid.EnableEditing( True )
		self.phd_grid.EnableGridLines( True )
		self.phd_grid.EnableDragGridSize( False )
		self.phd_grid.SetMargins( 0, 0 )
		
		# Columns
		self.phd_grid.EnableDragColMove( False )
		self.phd_grid.EnableDragColSize( True )
		self.phd_grid.SetColLabelSize( 30 )
		self.phd_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.phd_grid.EnableDragRowSize( True )
		self.phd_grid.SetRowLabelSize( 80 )
		self.phd_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.phd_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer6.Add( self.phd_grid, 4, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer6, 2, wx.EXPAND, 5 )
		
		
		self.phd_panel.SetSizer( bSizer11 )
		self.phd_panel.Layout()
		bSizer11.Fit( self.phd_panel )
		self.notebook.AddPage( self.phd_panel, u"PHD", False )
		self.spe_panel = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer121 = wx.BoxSizer( wx.VERTICAL )
		
		self.spe_fig = wxMatplotlib.Figure(self.spe_panel, xlabel='Wavelength (nm)', ylabel='Intensity (arb. units)')
		bSizer121.Add( self.spe_fig.canvas, 7, wx.EXPAND, 5 )
		
		self.spe_toolbar = wxMatplotlib.Toolbar( self.spe_fig.canvas )
		bSizer121.Add( self.spe_toolbar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5 )
		
		
		bSizer111.Add( bSizer121, 3, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.spe_checkbox_legend = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Legend@", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.spe_checkbox_legend, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		spe_choice_legend_locChoices = [ u"1", u"2", u"3", u"4", u"5", u"6" ]
		self.spe_choice_legend_loc = wx.Choice( self.spe_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 45,-1 ), spe_choice_legend_locChoices, 0 )
		self.spe_choice_legend_loc.SetSelection( 0 )
		self.spe_choice_legend_loc.SetMaxSize( wx.Size( 45,-1 ) )
		
		bSizer51.Add( self.spe_choice_legend_loc, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer51.AddSpacer( ( 0, 0), 2, wx.EXPAND, 5 )
		
		self.spe_checkbox_normalize = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Normalize", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer51.Add( self.spe_checkbox_normalize, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 0 )
		
		
		bSizer61.Add( bSizer51, 0, wx.EXPAND, 0 )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.spe_checkbox_countspersecond = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Counts per second", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.spe_checkbox_countspersecond, 0, wx.ALL, 5 )
		
		
		bSizer28.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.spe_checkbox_semilog = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Semilog", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer28.Add( self.spe_checkbox_semilog, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer61.Add( bSizer28, 0, wx.EXPAND, 0 )
		
		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.spe_checkbox_autoscale_on_drop = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Autoscale on drop", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.spe_checkbox_autoscale_on_drop.SetValue(True) 
		bSizer29.Add( self.spe_checkbox_autoscale_on_drop, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		
		bSizer29.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.spe_checkbox_raman = wx.CheckBox( self.spe_panel, wx.ID_ANY, u"Raman", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer29.Add( self.spe_checkbox_raman, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer61.Add( bSizer29, 0, wx.EXPAND, 0 )
		
		self.spe_grid = wx.grid.Grid( self.spe_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.spe_grid.CreateGrid( 0, 5 )
		self.spe_grid.EnableEditing( True )
		self.spe_grid.EnableGridLines( True )
		self.spe_grid.EnableDragGridSize( True )
		self.spe_grid.SetMargins( 0, 0 )
		
		# Columns
		self.spe_grid.AutoSizeColumns()
		self.spe_grid.EnableDragColMove( False )
		self.spe_grid.EnableDragColSize( True )
		self.spe_grid.SetColLabelSize( 30 )
		self.spe_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.spe_grid.EnableDragRowSize( True )
		self.spe_grid.SetRowLabelSize( 80 )
		self.spe_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.spe_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer61.Add( self.spe_grid, 2, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer111.Add( bSizer61, 2, wx.EXPAND, 5 )
		
		
		self.spe_panel.SetSizer( bSizer111 )
		self.spe_panel.Layout()
		bSizer111.Fit( self.spe_panel )
		self.notebook.AddPage( self.spe_panel, u"SPE", True )
		
		bSizer10.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.menubar = wx.MenuBar( 0 )
		self.menu_edit = wx.Menu()
		self.menu_edit_axes = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Axes", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.AppendItem( self.menu_edit_axes )
		
		self.menu_edit_clear_plot = wx.MenuItem( self.menu_edit, wx.ID_ANY, u"Clear plot", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_edit.AppendItem( self.menu_edit_clear_plot )
		
		self.menubar.Append( self.menu_edit, u"Edit" ) 
		
		self.SetMenuBar( self.menubar )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.phd_checkbox_legend.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_legend )
		self.phd_choice_legend_loc.Bind( wx.EVT_CHOICE, self.on_choice_phd_legend_location )
		self.phd_checkbox_normalize.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_normalize )
		self.phd_checkbox_countspersecond.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_countspersecond )
		self.phd_checkbox_semilog.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_semilog )
		self.phd_checkbox_autoscale_on_drop.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_autoscale_on_drop )
		self.phd_checkbox_offset_all.Bind( wx.EVT_CHECKBOX, self.on_checked_phd_offset_all_same )
		self.phd_offset_slider.Bind( wx.EVT_SCROLL, self.on_scroll_phd_offset_slider )
		self.phd_grid.Bind( wx.grid.EVT_GRID_CELL_CHANGE, self.on_phd_grid_edit )
		self.phd_grid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_phd_grid_leftclick )
		self.phd_grid.Bind( wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_phd_grid_rightclick )
		self.phd_grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_phd_grid_label_leftclick )
		self.phd_grid.Bind( wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_phd_grid_label_rightclick )
		self.spe_checkbox_legend.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_legend )
		self.spe_choice_legend_loc.Bind( wx.EVT_CHOICE, self.on_choice_spe_legend_location )
		self.spe_checkbox_normalize.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_normalize )
		self.spe_checkbox_countspersecond.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_countspersecond )
		self.spe_checkbox_semilog.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_semilog )
		self.spe_checkbox_autoscale_on_drop.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_autoscale_on_drop )
		self.spe_checkbox_raman.Bind( wx.EVT_CHECKBOX, self.on_checked_spe_raman )
		self.spe_grid.Bind( wx.grid.EVT_GRID_CELL_CHANGE, self.on_spe_grid_edit )
		self.spe_grid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_spe_grid_leftclick )
		self.spe_grid.Bind( wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_spe_grid_rightclick )
		self.spe_grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_spe_grid_label_leftclick )
		self.spe_grid.Bind( wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_spe_grid_label_rightclick )
		self.Bind( wx.EVT_MENU, self.on_menu_edit_axes, id = self.menu_edit_axes.GetId() )
		self.Bind( wx.EVT_MENU, self.on_menu_edit_clear_plot, id = self.menu_edit_clear_plot.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_checked_phd_legend( self, event ):
		event.Skip()
	
	def on_choice_phd_legend_location( self, event ):
		event.Skip()
	
	def on_checked_phd_normalize( self, event ):
		event.Skip()
	
	def on_checked_phd_countspersecond( self, event ):
		event.Skip()
	
	def on_checked_phd_semilog( self, event ):
		event.Skip()
	
	def on_checked_phd_autoscale_on_drop( self, event ):
		event.Skip()
	
	def on_checked_phd_offset_all_same( self, event ):
		event.Skip()
	
	def on_scroll_phd_offset_slider( self, event ):
		event.Skip()
	
	def on_phd_grid_edit( self, event ):
		event.Skip()
	
	def on_phd_grid_leftclick( self, event ):
		event.Skip()
	
	def on_phd_grid_rightclick( self, event ):
		event.Skip()
	
	def on_phd_grid_label_leftclick( self, event ):
		event.Skip()
	
	def on_phd_grid_label_rightclick( self, event ):
		event.Skip()
	
	def on_checked_spe_legend( self, event ):
		event.Skip()
	
	def on_choice_spe_legend_location( self, event ):
		event.Skip()
	
	def on_checked_spe_normalize( self, event ):
		event.Skip()
	
	def on_checked_spe_countspersecond( self, event ):
		event.Skip()
	
	def on_checked_spe_semilog( self, event ):
		event.Skip()
	
	def on_checked_spe_autoscale_on_drop( self, event ):
		event.Skip()
	
	def on_checked_spe_raman( self, event ):
		event.Skip()
	
	def on_spe_grid_edit( self, event ):
		event.Skip()
	
	def on_spe_grid_leftclick( self, event ):
		event.Skip()
	
	def on_spe_grid_rightclick( self, event ):
		event.Skip()
	
	def on_spe_grid_label_leftclick( self, event ):
		event.Skip()
	
	def on_spe_grid_label_rightclick( self, event ):
		event.Skip()
	
	def on_menu_edit_axes( self, event ):
		event.Skip()
	
	def on_menu_edit_clear_plot( self, event ):
		event.Skip()
	

###########################################################################
## Class LifetimeFitFrame
###########################################################################

class LifetimeFitFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Fit Lifetime", pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"File name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer12.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.phdfit_fname = wx.StaticText( self.m_panel2, wx.ID_ANY, u"blank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.phdfit_fname.Wrap( -1 )
		bSizer12.Add( self.phdfit_fname, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText31 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Dir.:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer121.Add( self.m_staticText31, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.phdfit_directory = wx.StaticText( self.m_panel2, wx.ID_ANY, u"blank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.phdfit_directory.Wrap( -1 )
		bSizer121.Add( self.phdfit_directory, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer121, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Start of fit (ns):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer8.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.phdfit_txtctrl_fitstart = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"0.0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.phdfit_txtctrl_fitstart.SetMaxLength( 0 ) 
		bSizer8.Add( self.phdfit_txtctrl_fitstart, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.phdfit_spinbutton_fitstart = wx.SpinButton( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.SP_WRAP )
		bSizer8.Add( self.phdfit_spinbutton_fitstart, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.phdfit_slider_fitstart = wx.Slider( self.m_panel2, wx.ID_ANY, 0, 0, 13600, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SL_HORIZONTAL )
		bSizer8.Add( self.phdfit_slider_fitstart, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Number of exponentials:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer9.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		phdfit_choice_number_exponentialsChoices = [ u"1", u"2", u"3" ]
		self.phdfit_choice_number_exponentials = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, phdfit_choice_number_exponentialsChoices, 0 )
		self.phdfit_choice_number_exponentials.SetSelection( 0 )
		bSizer9.Add( self.phdfit_choice_number_exponentials, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer9.AddSpacer( ( 0, 0), 2, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.phdfit_fitparams_grid = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.phdfit_fitparams_grid.CreateGrid( 3, 3 )
		self.phdfit_fitparams_grid.EnableEditing( True )
		self.phdfit_fitparams_grid.EnableGridLines( True )
		self.phdfit_fitparams_grid.EnableDragGridSize( False )
		self.phdfit_fitparams_grid.SetMargins( 0, 0 )
		
		# Columns
		self.phdfit_fitparams_grid.SetColSize( 0, 110 )
		self.phdfit_fitparams_grid.SetColSize( 1, 90 )
		self.phdfit_fitparams_grid.SetColSize( 2, 90 )
		self.phdfit_fitparams_grid.EnableDragColMove( False )
		self.phdfit_fitparams_grid.EnableDragColSize( True )
		self.phdfit_fitparams_grid.SetColLabelSize( 30 )
		self.phdfit_fitparams_grid.SetColLabelValue( 0, u"Lifetime (ns)" )
		self.phdfit_fitparams_grid.SetColLabelValue( 1, u"Amp." )
		self.phdfit_fitparams_grid.SetColLabelValue( 2, u"Offset" )
		self.phdfit_fitparams_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.phdfit_fitparams_grid.EnableDragRowSize( True )
		self.phdfit_fitparams_grid.SetRowLabelSize( 80 )
		self.phdfit_fitparams_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.phdfit_fitparams_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer7.Add( self.phdfit_fitparams_grid, 0, wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.phdfit_button_refit = wx.Button( self.m_panel2, wx.ID_ANY, u"Re-fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.phdfit_button_refit, 0, wx.ALL, 5 )
		
		self.phdfit_button_close = wx.Button( self.m_panel2, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.phdfit_button_close, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer7 )
		self.m_panel2.Layout()
		bSizer7.Fit( self.m_panel2 )
		bSizer6.Add( self.m_panel2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close_LifetimeFitFrame )
		self.phdfit_txtctrl_fitstart.Bind( wx.EVT_TEXT, self.on_phdfit_txtctrl_fitstart_changed )
		self.phdfit_spinbutton_fitstart.Bind( wx.EVT_SPIN_DOWN, self.on_phdfit_button_spinbutton_spindown )
		self.phdfit_spinbutton_fitstart.Bind( wx.EVT_SPIN_UP, self.on_phdfit_button_spinbutton_spinup )
		self.phdfit_slider_fitstart.Bind( wx.EVT_SCROLL, self.on_phdfit_slider_fitstart_changed )
		self.phdfit_choice_number_exponentials.Bind( wx.EVT_CHOICE, self.on_phdfit_choice_numexp_changed )
		self.phdfit_button_refit.Bind( wx.EVT_BUTTON, self.on_phdfit_button_refit_clicked )
		self.phdfit_button_close.Bind( wx.EVT_BUTTON, self.on_phdfit_button_close_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_close_LifetimeFitFrame( self, event ):
		event.Skip()
	
	def on_phdfit_txtctrl_fitstart_changed( self, event ):
		event.Skip()
	
	def on_phdfit_button_spinbutton_spindown( self, event ):
		event.Skip()
	
	def on_phdfit_button_spinbutton_spinup( self, event ):
		event.Skip()
	
	def on_phdfit_slider_fitstart_changed( self, event ):
		event.Skip()
	
	def on_phdfit_choice_numexp_changed( self, event ):
		event.Skip()
	
	def on_phdfit_button_refit_clicked( self, event ):
		event.Skip()
	
	def on_phdfit_button_close_clicked( self, event ):
		event.Skip()
	

###########################################################################
## Class SPEFitFrame
###########################################################################

class SPEFitFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Fit Lorentzians", pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.panel, wx.ID_ANY, u"File name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer12.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.spefit_fname = wx.StaticText( self.panel, wx.ID_ANY, u"blank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.spefit_fname.Wrap( -1 )
		bSizer12.Add( self.spefit_fname, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText31 = wx.StaticText( self.panel, wx.ID_ANY, u"Dir.:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer121.Add( self.m_staticText31, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )
		
		self.spefit_directory = wx.StaticText( self.panel, wx.ID_ANY, u"blank", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.spefit_directory.Wrap( -1 )
		bSizer121.Add( self.spefit_directory, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer121, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.panel, wx.ID_ANY, u"Domain of fit (nm):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer8.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.spefit_txtctrl_fitstart = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.spefit_txtctrl_fitstart.SetMaxLength( 0 ) 
		bSizer8.Add( self.spefit_txtctrl_fitstart, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText24 = wx.StaticText( self.panel, wx.ID_ANY, u"to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		bSizer8.Add( self.m_staticText24, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spefit_txtctrl_fitend = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.spefit_txtctrl_fitend.SetMaxLength( 0 ) 
		bSizer8.Add( self.spefit_txtctrl_fitend, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.panel, wx.ID_ANY, u"Number of Lorentzians:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer9.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_numlorentziansChoices = [ u"1", u"2", u"3" ]
		self.choice_numlorentzians = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_numlorentziansChoices, 0 )
		self.choice_numlorentzians.SetSelection( 0 )
		bSizer9.Add( self.choice_numlorentzians, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer9.AddSpacer( ( 0, 0), 2, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.checkbox_level = wx.CheckBox( self.panel, wx.ID_ANY, u"Level", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.checkbox_level, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.panel, wx.ID_ANY, u"Number of points:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		bSizer34.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		spefit_combo_numberpoints_levelChoices = [ u"1", u"4", u"10", u"25", u"50" ]
		self.spefit_combo_numberpoints_level = wx.ComboBox( self.panel, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, spefit_combo_numberpoints_levelChoices, 0 )
		self.spefit_combo_numberpoints_level.SetMaxSize( wx.Size( 75,-1 ) )
		
		bSizer34.Add( self.spefit_combo_numberpoints_level, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer34, 1, wx.EXPAND, 5 )
		
		self.grid = wx.grid.Grid( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.grid.CreateGrid( 1, 4 )
		self.grid.EnableEditing( True )
		self.grid.EnableGridLines( True )
		self.grid.EnableDragGridSize( False )
		self.grid.SetMargins( 0, 0 )
		
		# Columns
		self.grid.SetColSize( 0, 110 )
		self.grid.SetColSize( 1, 90 )
		self.grid.SetColSize( 2, 90 )
		self.grid.EnableDragColMove( False )
		self.grid.EnableDragColSize( True )
		self.grid.SetColLabelSize( 30 )
		self.grid.SetColLabelValue( 0, u"Center (nm)" )
		self.grid.SetColLabelValue( 1, u"Height" )
		self.grid.SetColLabelValue( 2, u"Q" )
		self.grid.SetColLabelValue( 3, u"Offset" )
		self.grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.grid.EnableDragRowSize( True )
		self.grid.SetRowLabelSize( 80 )
		self.grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer7.Add( self.grid, 0, wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.spefit_button_fit = wx.Button( self.panel, wx.ID_ANY, u"Fit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.spefit_button_fit, 0, wx.ALL, 5 )
		
		self.spefit_button_close = wx.Button( self.panel, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.spefit_button_close, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		self.panel.SetSizer( bSizer7 )
		self.panel.Layout()
		bSizer7.Fit( self.panel )
		bSizer6.Add( self.panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.choice_numlorentzians.Bind( wx.EVT_CHOICE, self.on_choice_numlorentzians_changed )
		self.grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_grid_label_leftclick )
		self.grid.Bind( wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.on_spefit_grid_label_rightclick )
		self.spefit_button_fit.Bind( wx.EVT_BUTTON, self.on_spefit_button_fit_clicked )
		self.spefit_button_close.Bind( wx.EVT_BUTTON, self.on_spefit_button_close_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_choice_numlorentzians_changed( self, event ):
		event.Skip()
	
	def on_grid_label_leftclick( self, event ):
		event.Skip()
	
	def on_spefit_grid_label_rightclick( self, event ):
		event.Skip()
	
	def on_spefit_button_fit_clicked( self, event ):
		event.Skip()
	
	def on_spefit_button_close_clicked( self, event ):
		event.Skip()
	

###########################################################################
## Class SPEFit_SliderFrame
###########################################################################

class SPEFit_SliderFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 475,125 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.spefit_popup_slider = wx.Slider( self.m_panel5, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer26.Add( self.spefit_popup_slider, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer28.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.spefit_popup_button_okay = wx.Button( self.m_panel5, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.spefit_popup_button_okay, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spefit_popup_button_cancel = wx.Button( self.m_panel5, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.spefit_popup_button_cancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer26.Add( bSizer28, 1, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer26 )
		self.m_panel5.Layout()
		bSizer26.Fit( self.m_panel5 )
		bSizer25.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer25 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.spefit_popup_slider.Bind( wx.EVT_SCROLL, self.on_spefit_popup_slider_scroll )
		self.spefit_popup_button_okay.Bind( wx.EVT_BUTTON, self.on_spefit_popup_button_okay_clicked )
		self.spefit_popup_button_cancel.Bind( wx.EVT_BUTTON, self.on_spefit_popup_button_cancel_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_spefit_popup_slider_scroll( self, event ):
		event.Skip()
	
	def on_spefit_popup_button_okay_clicked( self, event ):
		event.Skip()
	
	def on_spefit_popup_button_cancel_clicked( self, event ):
		event.Skip()
	

