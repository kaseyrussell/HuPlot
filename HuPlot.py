#!/usr/bin/python
"""GUI plotting program built with wxFormBuilder.
   --Kasey J. Russell, SEAS Harvard
   """

import matplotlib
if matplotlib.get_backend() != 'WXAgg':
    """ This conditional is just to check if it's loaded so that python doesn't
        complain. If it already was loaded and set to a different backend, 
        we couldn't change it anyway (which is why python issues a warning if
        we use the 'use' method and a backend has already been loaded).
    """
    matplotlib.use('WXAgg')

import pylab
import numpy as np
import kasey_fitspectra
import wx
import HuPlot_GUI
import cPickle
import gzip
import kasey_utils as kc
import os.path
import PicoQuantUtils as pq
import winspec
from wx.lib.dialogs import textEntryDialog, messageDialog

class MainApp( wx.App ): 
    """ The main application event loop. """

    def __init__( self, redirect=False, filename=None ):
        wx.App.__init__( self, redirect, filename )
        self.Bind( wx.EVT_CLOSE, self.on_close_HuPlot )
        
        self.mainframe = HuPlot( None )
        self.mainframe.Show( True )
    
    def on_close_HuPlot( self, event ):
        self.Destroy()



class HuPlot( HuPlot_GUI.HuPlot_GUI ):
    """ Implementation of HuPlot_GUI, the main window frame. """

    def __init__( self, parent ):
        HuPlot_GUI.HuPlot_GUI.__init__( self, parent )
        self.phd_grid.SetRowLabelSize(35)
        
        self.phd_fig.canvas.SetDropTarget( FileDropTarget(self.phd_fig.canvas, self) )        
        self.spe_fig.canvas.SetDropTarget( FileDropTarget(self.spe_fig.canvas, self) )        

        self.phd_grid.GetGridWindow().SetDropTarget( FileDropTarget(self.phd_grid, self) )
        self.spe_grid.GetGridWindow().SetDropTarget( FileDropTarget(self.spe_grid, self) )
        
        self.phd_fig.canvas.mpl_connect( 'button_release_event', self.on_click_in_phd_fig )
        self.phd_fig.canvas.mpl_connect( 'motion_notify_event', self.on_move_in_phd_fig )
        self.phd_fig.canvas.mpl_connect( 'axes_leave_event', self.on_leave_phd_fig )

        self.spe_fig.canvas.mpl_connect( 'button_press_event', self.on_click_press_in_spe_fig )
        self.spe_fig.canvas.mpl_connect( 'button_release_event', self.on_click_release_in_spe_fig )
        self.spe_fig.canvas.mpl_connect( 'motion_notify_event', self.on_move_in_spe_fig )
        self.spe_fig.canvas.mpl_connect( 'axes_leave_event', self.on_leave_spe_fig )

        self.row_label_column = -1 # set by wxpython; named here for clarity

        self.mpl_right_mouse_button = 3

        self.phd_color_column = 0
        self.phd_label_column = 2
        self.phd_offset_column = 1
        self.phd_grid.SetColLabelValue( self.phd_color_column, '' )
        self.phd_grid.SetColSize( self.phd_color_column, 30 )
        self.phd_grid.SetColLabelValue( self.phd_label_column, 'Label' )
        self.phd_grid.SetColSize( self.phd_label_column, 250 )
        self.phd_grid.SetColLabelValue( self.phd_offset_column, 'Offset' )
        self.phd_grid.SetColSize( self.phd_offset_column, 50 )
        self.phd_grid.SetDefaultCellOverflow( False )

        self.phd_line_list = []
        self.phd_normalize = self.phd_checkbox_normalize.IsChecked()
        self.phd_countspersecond = self.phd_checkbox_countspersecond.IsChecked()
        self.phd_semilog = self.phd_checkbox_semilog.IsChecked()
        self.phd_offset_all = self.phd_checkbox_offset_all.IsChecked()
        self.phd_offset = 0.0
        self.phd_autoscale_on_drop = True
        
        self.spe_color_column = 0
        self.spe_label_column = 4
        self.spe_bg_column = 1
        self.spe_offset_column = 2
        self.spe_laser_column = 3
        self.spe_grid.SetColLabelValue( self.spe_color_column, '' )
        self.spe_grid.SetColSize( self.spe_color_column, 30 )
        self.spe_grid.SetColLabelValue( self.spe_label_column, 'Label' )
        self.spe_grid.SetColSize( self.spe_label_column, 250 )
        self.spe_grid.SetColLabelValue( self.spe_bg_column, 'bg' )
        self.spe_grid.SetColSize( self.spe_bg_column, 30 )
        self.spe_grid.SetColLabelValue( self.spe_offset_column, '+y')
        self.spe_grid.SetColSize( self.spe_offset_column, 30 )
        self.spe_grid.SetColLabelValue( self.spe_laser_column, 'laser')
        self.spe_grid.SetColSize( self.spe_laser_column, 40 )
        self.spe_grid.SetDefaultCellOverflow( False )

        self.spe_line_list         = []
        self.spe_bg_list           = []
        self.spe_normalize         = self.spe_checkbox_normalize.IsChecked()
        self.spe_countspersecond   = self.spe_checkbox_countspersecond.IsChecked()
        self.spe_semilog           = self.spe_checkbox_semilog.IsChecked()
        self.spe_raman             = self.spe_checkbox_raman.IsChecked()
        self.spe_autoscale_on_drop = True
        self.spe_offset            = 0.0

        self.color_data = wx.ColourData()
        self.default_path = None
        self.lifetime_fit_frame = None
        self.spe_fit_frame = None

    def phd_delete_row( self, event ):
        """Remove a trace from the trace list."""
        del self.phd_line_list[ self.current_row ]
        self.phd_grid.DeleteRows( pos=self.current_row, numRows=1 )
        if event is not None: self.phd_update_plot()


    def spe_delete_row( self, event ):
        """Remove a spectrum from the spectrum list."""
        del self.spe_line_list[ self.current_row ]
        self.spe_grid.DeleteRows( pos=self.current_row, numRows=1 )
        if event is not None: self.spe_update_plot()


    def phd_set_color_multiple_rows(self, event):
        """Set color for multiple data files at once."""
        color = self.get_color( self.phd_grid.GetSelectedRows()[0] )
        if color is not None:
            for row in self.phd_grid.GetSelectedRows():
                self.phd_set_color( row, color, update_plot=False )
            self.phd_update_plot()
            self.Refresh()


    def spe_set_color_multiple_rows(self, event):
        """Set color for multiple data files at once."""
        color = self.get_color( self.spe_grid.GetSelectedRows()[0] )
        if color is not None:
            for row in self.spe_grid.GetSelectedRows():
                self.spe_set_color( row, color, update_plot=False )
            self.spe_update_plot()
            self.Refresh()


    def phd_set_label_multiple_rows(self, event):
        """Set label for multiple data files at once."""
        dialog = textEntryDialog(self, message='Label:',
            title='Set label for selected rows', defaultText='')
        if not dialog.accepted: return None
        for row in self.phd_grid.GetSelectedRows():
            self.phd_line_list[row]['label'] = dialog.text
            self.phd_grid.SetCellValue( row, self.phd_label_column, dialog.text )
        self.on_checked_phd_legend( event=None )


    def spe_set_label_multiple_rows(self, event):
        """Set label for multiple data files at once."""
        dialog = textEntryDialog(self, message='Label:',
            title='Set label for selected rows', defaultText='')
        if not dialog.accepted: return None
        for row in self.spe_grid.GetSelectedRows():
            self.spe_line_list[row]['label'] = dialog.text
            self.spe_grid.SetCellValue( row, self.spe_label_column, dialog.text )
        self.on_checked_spe_legend( event=None )

        
    def phd_delete_multiple_rows(self, event):
        """Delete multiple data files at once."""
        dlg = messageDialog(self, message='Delete selected rows?', title='Alert!')
        if not dlg.accepted: return None
        for row in reversed(self.phd_grid.GetSelectedRows()):
            self.current_row = row
            self.phd_delete_row( event=None )
        self.phd_update_plot()
        

    def spe_delete_multiple_rows(self, event):
        """Delete multiple data files at once."""
        dlg = messageDialog(self, message='Delete selected rows?', title='Alert!')
        if not dlg.accepted: return None
        for row in reversed(sorted(self.spe_grid.GetSelectedRows())):
            self.current_row = row
            self.spe_delete_row( event=None )
        self.spe_update_plot()
        

    def display_position( self, x, y ):
        """ Update statusbar field 1 (zero-indexed, of course) with the current
            mouse position
        """
        self.statusbar.SetStatusText( "x:"+str(x)+", y:"+str(y) )


    def phd_fit_row( self, event ):
        """Launch the fit window."""
        self.lifetime_fit_frame = LifetimeFitFrame( parent=self )
        self.lifetime_fit_frame.Show( True )


    def spe_fit_row( self, event ):
        """Launch the fit window."""
        self.spe_fit_frame = SPEFitFrame( parent=self )
        self.spe_fit_frame.Show( True )


    def get_phd_tab_is_active( self ):
        """Returns bool indicating whether the phd tab is active."""
        return self.notebook.GetSelection() == 0
        
        
    def get_spe_tab_is_active( self ):
        """Returns bool indicating whether the spe tab is active."""
        return self.notebook.GetSelection() == 1
        

    def get_color( self, row ):
        """
        This is mostly from the wxPython Demo! Pops up a color-picker dialog window.
        """
        if self.get_phd_tab_is_active():
            self.color_data.SetColour( wx.Colour( *self.phd_line_list[row]['color'] ))
        elif self.get_spe_tab_is_active():
            self.color_data.SetColour( wx.Colour( *self.spe_line_list[row]['color'] ))
            
        dlg = wx.ColourDialog( self, self.color_data )
 
        # Ensure the full colour dialog is displayed, 
        # not the abbreviated version.
        dlg.GetColourData().SetChooseFull(True)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            color = data.GetColour().Get()
            #print 'You selected: %s\n' % str(color)
        else:
            color=None
            
        dlg.Destroy()
        return color


    def on_checked_phd_countspersecond( self, event ):
        """ Event handler. """
        self.phd_clear_bestfit_lines()
        if isinstance(self.lifetime_fit_frame, LifetimeFitFrame):
            self.lifetime_fit_frame.on_close_LifetimeFitFrame( None )

        if self.phd_checkbox_countspersecond.IsChecked():
            self.phd_countspersecond = True
            self.phd_update_plot()
        else:
            self.phd_countspersecond = False
            self.phd_update_plot()
    

    def on_checked_spe_countspersecond( self, event ):
        if self.spe_checkbox_countspersecond.IsChecked():
            if self.spe_checkbox_normalize.IsChecked():
                self.spe_checkbox_normalize.SetValue(False)
                self.on_checked_spe_normalize(None)
            self.spe_countspersecond = True
            self.spe_update_plot()
        else:
            self.spe_countspersecond = False
            for line in self.spe_line_list:
                spectrum = line['spectrum']
                spectrum.reset_lum()
            if event is not None: self.spe_update_plot()
    

    def on_checked_phd_legend( self, event ):
        """ Event handler. """
        if self.phd_checkbox_legend.IsChecked():
            handles, labels = self.phd_fig.axes.get_legend_handles_labels()
            # reset labels to match the grid in case we haven't replotted since a change:
            for i,line in enumerate( self.phd_line_list ):
                labels[i] = line['label']
            self.phd_fig_legend = self.phd_fig.axes.legend( handles, labels, loc=self.phd_choice_legend_loc.GetSelection()+1 )
            self.phd_fig_legend.draggable(state=True, use_blit=True)
            self.phd_fig.canvas.draw()
        else:
            self.phd_fig.axes.legend_ = None
            self.phd_fig_legend = None
            self.phd_fig.canvas.draw()
    

    def on_checked_spe_legend( self, event ):
        """ Event handler. """
        if self.spe_checkbox_legend.IsChecked():
            handles, labels = self.spe_fig.axes.get_legend_handles_labels()
            # reset labels to match the grid in case we haven't replotted since a change:
            for i,line in enumerate( self.spe_line_list ):
                labels[i] = line['label']
            self.spe_fig.axes.legend( handles, labels, loc=self.spe_choice_legend_loc.GetSelection()+1 )
            self.spe_fig.canvas.draw()
        else:
            self.spe_fig.axes.legend_ = None
            self.spe_fig.canvas.draw()
    

    def on_choice_phd_legend_location( self, event ):
        """ Event handler. """
        self.on_checked_phd_legend( None )
    

    def on_choice_spe_legend_location( self, event ):
        """ Event handler. """
        self.on_checked_spe_legend( None )
    

    def on_checked_phd_autoscale_on_drop( self, event ):
        """ Event handler. """
        if self.phd_checkbox_autoscale_on_drop.IsChecked():
            self.phd_autoscale_on_drop = True
        else:
            self.phd_autoscale_on_drop = False


    def on_checked_spe_autoscale_on_drop( self, event ):
        """ Event handler. """
        if self.spe_checkbox_autoscale_on_drop.IsChecked():
            self.spe_autoscale_on_drop = True
        else:
            self.spe_autoscale_on_drop = False

    
    def on_checked_phd_normalize( self, event ):
        """ Event handler. """
        self.phd_clear_bestfit_lines()
        if isinstance(self.lifetime_fit_frame, LifetimeFitFrame):
            self.lifetime_fit_frame.on_close_LifetimeFitFrame( None )
        if self.phd_checkbox_normalize.IsChecked():
            self.phd_normalize = True
            self.phd_update_plot()
        else:
            self.phd_normalize = False
            self.phd_update_plot()
    

    def on_checked_spe_normalize( self, event ):
        """ Event handler. """
        if self.spe_checkbox_normalize.IsChecked():
            if self.spe_checkbox_countspersecond.IsChecked():
                self.spe_checkbox_countspersecond.SetValue(False)
                self.on_checked_spe_countspersecond(None)
            self.spe_normalize = True
            self.spe_update_plot()
        else:
            self.spe_normalize = False
            for line in self.spe_line_list:
                spectrum = line['spectrum']
                spectrum.reset_lum()
            if event is not None: self.spe_update_plot()

    
    def on_checked_spe_raman( self, event ):
        """ Event handler. """
        if self.spe_checkbox_raman.IsChecked():
            self.spe_raman = True
            self.spe_update_plot()
        else:
            self.spe_raman = False
            if event is not None: self.spe_update_plot()

    
    def on_checked_phd_offset_all_same( self, event ):
        """ Event handler. """
        if self.phd_checkbox_offset_all.IsChecked():
            self.phd_offset_all = True
            if len( self.phd_line_list ) > 0:
                self.phd_offset_slider.Value = 1000*self.phd_line_list[-1]['offset']
            self.phd_update_plot()
        else:
            self.phd_offset_all = False
            self.phd_update_plot()

    
    def on_scroll_phd_offset_slider( self, event ):
        """ Event handler. """
        self.phd_clear_bestfit_lines()
        if isinstance(self.lifetime_fit_frame, LifetimeFitFrame):
            self.lifetime_fit_frame.on_close_LifetimeFitFrame( None )
        offset = float(self.phd_offset_slider.Value)/1000.0
        if self.phd_offset_all:
            self.phd_offset = offset
            for line in self.phd_line_list:
                line['offset'] = offset
                self.phd_grid.SetCellValue( line['row'], self.phd_offset_column, str(offset) )
        self.phd_update_plot()
    

    def on_checked_phd_semilog( self, event ):
        """ Event handler. """
        if isinstance(self.lifetime_fit_frame, LifetimeFitFrame):
            self.lifetime_fit_frame.on_close_LifetimeFitFrame( None )
        if self.phd_checkbox_semilog.IsChecked():
            self.phd_semilog = True
            self.phd_update_plot()
        else:
            self.phd_semilog = False
            self.phd_update_plot()


    def on_checked_spe_semilog( self, event ):
        """ Event handler. """
        if self.spe_checkbox_semilog.IsChecked():
            self.spe_semilog = True
            self.spe_update_plot()
        else:
            self.spe_semilog = False
            self.spe_update_plot()
    

    def on_click_in_phd_fig( self, event ):
        """ Event handler. """
        if event.button == self.mpl_right_mouse_button:
            if not hasattr(self, "popup_clear"):
                self.popup_clear = wx.NewId()
     
            menu = wx.Menu()
            menu.AppendItem( wx.MenuItem( menu, self.popup_clear, "Clear plot" ) )
            wx.EVT_MENU( self, self.popup_clear, self.on_menu_edit_clear_phd_plot )
            
            self.PopupMenu(menu)
            menu.Destroy()


    def on_click_press_in_spe_fig( self, event ):
        """ Event handler. """
        pass

    def on_click_release_in_spe_fig( self, event ):
        """ Event handler. """
        if event.button == self.mpl_right_mouse_button:
            if not hasattr(self, "popup_clear"):
                self.popup_clear = wx.NewId()
     
            menu = wx.Menu()
            menu.AppendItem( wx.MenuItem( menu, self.popup_clear, "Clear plot" ) )
            wx.EVT_MENU( self, self.popup_clear, self.on_menu_edit_clear_spe_plot )
            
            self.PopupMenu(menu)
            menu.Destroy()


    def on_leave_phd_fig( self, event ):
        """ Event handler. """
        self.statusbar.SetStatusText( "" )


    def on_leave_spe_fig( self, event ):
        """ Event handler. """
        self.statusbar.SetStatusText( "" )


    def on_menu_edit_clear_phd_plot( self, event ):
        """ Event handler. """
        self.phd_line_list = []
        self.phd_grid.DeleteRows( numRows=self.phd_grid.GetNumberRows() )
        self.phd_update_plot()
    
    def on_menu_edit_clear_spe_plot( self, event ):
        """ Event handler. """
        self.spe_line_list = []
        self.spe_grid.DeleteRows( numRows=self.spe_grid.GetNumberRows() )
        self.spe_update_plot()
    
    
    def on_move_in_phd_fig( self, event ):
        """ Event handler. """
        if not event.inaxes: return True
        x = event.xdata
        y = event.ydata
        self.display_position( x, y )


    def on_move_in_spe_fig( self, event ):
        """ Event handler. """
        if not event.inaxes: return True
        x = event.xdata
        y = event.ydata
        self.display_position( x, y )


    def on_phd_grid_edit( self, event ):
        """ Event handler. """
        row = event.GetRow()
        col = event.GetCol()
        if col == self.phd_label_column:
            self.phd_line_list[row]['label'] = self.phd_grid.GetCellValue( row, self.phd_label_column )
            self.on_checked_phd_legend( event=None )
            
        elif col == self.phd_offset_column:
            if self.phd_offset_all:
                offset = float( self.phd_grid.GetCellValue( row, self.phd_offset_column ) )
                self.phd_offset = offset
                self.phd_offset_slider.Value = 1000*offset
                for line in self.phd_line_list:
                    line['offset'] = offset
                    self.phd_grid.SetCellValue( line['row'], self.phd_offset_column, str(offset) )
            else:
                self.phd_line_list[row]['offset'] = self.phd_grid.GetCellValue( row, self.phd_offset_column )
            self.phd_update_plot()

    
    def on_spe_grid_edit( self, event ):
        """ Event handler. """
        row = event.GetRow()
        col = event.GetCol()
        if col == self.spe_label_column:
            self.spe_line_list[row]['label'] = self.spe_grid.GetCellValue( row, self.spe_label_column )
            self.on_checked_spe_legend( event=None )
            
        elif col == self.spe_offset_column:
            self.spe_line_list[row]['offset'] = self.spe_grid.GetCellValue( row, self.spe_offset_column )
            self.spe_update_plot()
    
        elif col == self.spe_laser_column:
            self.spe_line_list[row]['spectrum'].laser = float(self.spe_grid.GetCellValue( row, self.spe_laser_column ))
            self.spe_update_plot()
    

    def on_phd_grid_leftclick( self, event ):
        """ Event handler. """
        row = event.GetRow()
        col = event.GetCol()
        
        if col == self.phd_color_column:
            color = self.get_color( row )
            if color is not None: self.phd_set_color( row, color )
                
        elif col == self.phd_label_column:
            self.phd_grid.SetGridCursor( row, col )

        elif col == self.phd_offset_column:
            self.phd_grid.SetGridCursor( row, col )
    
    
    def phd_set_color( self, row, color, update_plot=True ):
        """ Event handler. """
        self.phd_line_list[row]['color'] = color
        self.phd_grid.SetCellBackgroundColour( row, self.phd_color_column, color )
        if update_plot:
            self.phd_update_plot()
            self.Refresh()
        
        
    def spe_set_color( self, row, color, update_plot=True ):
        """ Event handler. """
        self.spe_line_list[row]['color'] = color
        self.spe_grid.SetCellBackgroundColour( row, self.spe_color_column, color )
        if update_plot:
            self.spe_update_plot()
            self.Refresh()
        

    def on_spe_grid_leftclick( self, event ):
        """ Event handler. """
        row = event.GetRow()
        col = event.GetCol()
        
        if col == self.spe_color_column:
            color = self.get_color( row )
            if color is not None: self.spe_set_color( row, color )

        elif col == self.spe_label_column:
            self.spe_grid.SetGridCursor( row, col )

        elif col == self.spe_offset_column:
            self.spe_grid.SetGridCursor( row, col )

        elif col == self.spe_laser_column:
            self.spe_grid.SetGridCursor( row, col )

    
    def on_phd_grid_rightclick( self, event ):
        """ Event handler. """
        if event.GetCol() == self.phd_label_column:
            if not hasattr(self, "popup_grid"):
                self.popup_grid = wx.NewId()
     
            self.current_cell = [event.GetRow(), event.GetCol()]
            menu = wx.Menu()
            menu.AppendItem( wx.MenuItem( menu, self.popup_grid, "Reset label" ) )
            wx.EVT_MENU( self, self.popup_grid, self.phd_reset_label )
            
            self.PopupMenu(menu)
            menu.Destroy()
    

    def on_spe_grid_rightclick( self, event ):
        """ Event handler. """
        if event.GetCol() == self.spe_label_column:
            if not hasattr(self, "popup_grid"):
                self.popup_grid = wx.NewId()
     
            self.current_cell = [event.GetRow(), event.GetCol()]
            menu = wx.Menu()
            menu.AppendItem( wx.MenuItem( menu, self.popup_grid, "Reset label" ) )
            wx.EVT_MENU( self, self.popup_grid, self.spe_reset_label )
            
            self.PopupMenu(menu)
            menu.Destroy()
    
    def on_phd_grid_rightclick_multiple_rows(self):
        """ Event handler. """
        if not hasattr(self, "popup_delete_multiple_rows"):
            self.popup_delete_multiple_rows = wx.NewId()
        if not hasattr(self, "popup_set_color_multiple_rows"):
            self.popup_set_color_multiple_rows = wx.NewId()
        if not hasattr(self, "popup_set_label_multiple_rows"):
            self.popup_set_label_multiple_rows = wx.NewId()
 
        
        menu = wx.Menu()

        set_color_multiple_rows = wx.MenuItem( menu, self.popup_set_color_multiple_rows, "Set selected colors" )
        menu.AppendItem( set_color_multiple_rows )
        wx.EVT_MENU( self, self.popup_set_color_multiple_rows, self.phd_set_color_multiple_rows )
        
        set_label_multiple_rows = wx.MenuItem( menu, self.popup_set_label_multiple_rows, "Set selected labels" )
        menu.AppendItem( set_label_multiple_rows )
        wx.EVT_MENU( self, self.popup_set_label_multiple_rows, self.phd_set_label_multiple_rows )
        
        delete_multiple_rows = wx.MenuItem( menu, self.popup_delete_multiple_rows, "Delete selected rows" )
        menu.AppendItem( delete_multiple_rows )
        wx.EVT_MENU( self, self.popup_delete_multiple_rows, self.phd_delete_multiple_rows )
        
        self.PopupMenu(menu)
        menu.Destroy()
        
    
    def on_spe_grid_rightclick_multiple_rows(self):
        """ Event handler. """
        if not hasattr(self, "popup_delete_multiple_rows"):
            self.popup_delete_multiple_rows = wx.NewId()
        if not hasattr(self, "popup_set_color_multiple_rows"):
            self.popup_set_color_multiple_rows = wx.NewId()
        if not hasattr(self, "popup_set_label_multiple_rows"):
            self.popup_set_label_multiple_rows = wx.NewId()
 
        
        menu = wx.Menu()

        set_color_multiple_rows = wx.MenuItem( menu, self.popup_set_color_multiple_rows, "Set selected colors" )
        menu.AppendItem( set_color_multiple_rows )
        wx.EVT_MENU( self, self.popup_set_color_multiple_rows, self.spe_set_color_multiple_rows )
        
        set_label_multiple_rows = wx.MenuItem( menu, self.popup_set_label_multiple_rows, "Set selected labels" )
        menu.AppendItem( set_label_multiple_rows )
        wx.EVT_MENU( self, self.popup_set_label_multiple_rows, self.spe_set_label_multiple_rows )
        
        delete_multiple_rows = wx.MenuItem( menu, self.popup_delete_multiple_rows, "Delete selected rows" )
        menu.AppendItem( delete_multiple_rows )
        wx.EVT_MENU( self, self.popup_delete_multiple_rows, self.spe_delete_multiple_rows )
        
        self.PopupMenu(menu)
        menu.Destroy()


    def on_phd_grid_label_leftclick( self, event ):
        """ Event handler. """
        if not event.ShiftDown() and not event.ControlDown():
            self.phd_grid.ClearSelection()
            self.phd_grid.SelectRow(event.Row,addToSelected=True)
        elif event.ShiftDown():
            if len(self.phd_grid.GetSelectedRows()) == 0:
                self.phd_grid.SelectRow(event.Row,addToSelected=True)
            else:
                first_selected = self.phd_grid.GetSelectedRows()[0]
                if event.Row > first_selected:
                    rows = range( first_selected+1, event.Row+1 )
                else:
                    rows = range( event.Row, first_selected )
                for row in rows:
                    self.phd_grid.SelectRow(row,addToSelected=True)
        elif event.ControlDown():
            if event.Row in self.phd_grid.GetSelectedRows():
                self.phd_grid.DeselectRow(event.Row)
            else:
                self.phd_grid.SelectRow(event.Row,addToSelected=True)
                
    def on_spe_grid_label_leftclick( self, event ):
        """ Event handler. """
        if not event.ShiftDown() and not event.ControlDown():
            self.spe_grid.ClearSelection()
            self.spe_grid.SelectRow(event.Row,addToSelected=True)
        elif event.ShiftDown():
            if len(self.spe_grid.GetSelectedRows()) == 0:
                self.spe_grid.SelectRow(event.Row,addToSelected=True)
            else:
                first_selected = self.spe_grid.GetSelectedRows()[0]
                if event.Row > first_selected:
                    rows = range( first_selected+1, event.Row+1 )
                else:
                    rows = range( event.Row, first_selected )
                for row in rows:
                    self.spe_grid.SelectRow(row,addToSelected=True)
        elif event.ControlDown():
            if event.Row in self.spe_grid.GetSelectedRows():
                self.spe_grid.DeselectRow(event.Row)
            else:
                self.spe_grid.SelectRow(event.Row,addToSelected=True)
                
                    

        
    def on_phd_grid_label_rightclick( self, event ):
        """ Event handler. """
        if len(self.phd_grid.GetSelectedRows()) > 1:
            self.on_phd_grid_rightclick_multiple_rows()
            
        elif event.GetCol() == self.row_label_column:
            if not hasattr(self, "popup_deleterow"):
                self.popup_deleterow = wx.NewId()
            if not hasattr(self, "popup_fitrow"):
                self.popup_fitrow = wx.NewId()
     
            self.current_row = event.GetRow()

            menu = wx.Menu()
            fit_row = wx.MenuItem( menu, self.popup_fitrow, "Fit" )
            menu.AppendItem( fit_row )
            wx.EVT_MENU( self, self.popup_fitrow, self.phd_fit_row )
            
            delete_row = wx.MenuItem( menu, self.popup_deleterow, "Delete row" )
            menu.AppendItem( delete_row )
            wx.EVT_MENU( self, self.popup_deleterow, self.phd_delete_row )
            
            self.PopupMenu(menu)
            menu.Destroy()


    def on_spe_grid_label_rightclick( self, event ):
        """ Event handler. """
        if len(self.spe_grid.GetSelectedRows()) > 1:
            self.on_spe_grid_rightclick_multiple_rows()
            
        elif event.GetCol() == self.row_label_column:
            if not hasattr(self, "popup_deleterow"):
                self.popup_deleterow = wx.NewId()
            if not hasattr(self, "popup_fitrow"):
                self.popup_fitrow = wx.NewId()
     
            self.current_row = event.GetRow()

            menu = wx.Menu()
            fit_row = wx.MenuItem( menu, self.popup_fitrow, "Fit" )
            menu.AppendItem( fit_row )
            wx.EVT_MENU( self, self.popup_fitrow, self.spe_fit_row )
            
            delete_row = wx.MenuItem( menu, self.popup_deleterow, "Delete row" )
            menu.AppendItem( delete_row )
            wx.EVT_MENU( self, self.popup_deleterow, self.spe_delete_row )
            
            self.PopupMenu(menu)
            menu.Destroy()

    
    def on_menu_edit_axes( self, event ):
        # TODO: Implement on_menu_edit_axes
        pass
    
    def on_menu_edit_clear_plot( self, event ):
        """ Clear the plot of whichever tab is currently displayed. """
        if self.get_phd_tab_is_active():
            self.on_menu_edit_clear_phd_plot(None)
        elif self.get_spe_tab_is_active():
            self.on_menu_edit_clear_spe_plot(None)
            
            
    def on_spe_txtctrl_offset_changed( self, event ):
        """ Event handler. """
        try:
            self.spe_offset = float( self.spe_txtctrl_offset.GetValue() )
        except ValueError:
            return True

        if self.spe_checkbox_offset.IsChecked():
            """ don't alter values unless checkbox is checked. """
            self.on_checked_spe_offset(None)


    def on_checked_spe_offset( self, event ):
        """ Event handler. """
        for i,line in enumerate(self.spe_line_list):
            offset = 0.0 if not self.spe_checkbox_offset.IsChecked() else i*self.spe_offset
            line['offset'] = offset
            self.spe_grid.SetCellValue( i, self.spe_offset_column, str(offset) )

        self.spe_update_plot()        


    def phd_clear_bestfit_lines( self ):
        """
        If you normalize the plot, etc., then obviously you will need
        to re-fit the data, so this voids the bestfit line.:
        """
        for row in range( self.phd_grid.GetNumberRows() ):
            s = self.phd_line_list[row]['trace']
            if hasattr( s, 'bestfit_line' ):
                del s.bestfit_line
                s.has_fit = False


    def phd_reset_label( self, event ):
        """ Resets the label to default value. """
        fname = self.phd_line_list[self.current_cell[0]]['fname']
        label = os.path.splitext( os.path.basename( fname ) )[0]
        self.phd_grid.SetCellValue(
            self.current_cell[0],
            self.phd_label_column,
            label )
        self.phd_line_list[self.current_cell[0]]['label'] = self.phd_grid.GetCellValue(
            self.current_cell[0],
            self.phd_label_column )
        self.on_checked_phd_legend( event=None )


    def phd_update_plot( self, just_dropped=0 ):
        """ Update plot. """
        xlim = self.phd_fig.axes.get_xlim()
        ylim = self.phd_fig.axes.get_ylim()

        if just_dropped>0 and not self.phd_autoscale_on_drop:
            self.phd_fig.axes.set_autoscale_on( False )
            for i in range( just_dropped ):
                line = self.phd_line_list[-(i+1)]
                s = line['trace']
                s.wrapcurves( float(line['offset']),
                        delete_firstpoints=1, delete_lastpoints=1,
                        use_raw=True )
                if self.phd_normalize: s.normalize_curves()
                if self.phd_countspersecond: s.counts_per_second()
                s.plot( color=[c/255.0 for c in line['color']],
                    label=line['label'],
                    semilogy=self.phd_semilog )
        else:
            self.phd_fig.axes.cla()
            self.phd_fig.axes.set_autoscale_on( True )
        
            for row in range( self.phd_grid.GetNumberRows() ):
                s = self.phd_line_list[row]['trace']
                s.wrapcurves( float(self.phd_line_list[row]['offset']),
                        delete_firstpoints=1, delete_lastpoints=1,
                        use_raw=True )
                if self.phd_normalize: s.normalize_curves()
                if self.phd_countspersecond: s.counts_per_second()
                s.plot( color=[c/255.0 for c in self.phd_line_list[row]['color']],
                          label=self.phd_line_list[row]['label'],
                          semilogy=self.phd_semilog )
                if hasattr( s, 'bestfit_line' ):
                    s.bestfit_line, = self.phd_fig.axes.plot(
                        s.t[0][pylab.find(s.t[0]>=s.fitstart)],
                        s.bestfit, '-k', scalex=False, scaley=False )
                
            
            self.phd_fig.axes.set_xlabel( 'Time (ns)' )
            self.phd_fig.axes.set_ylabel( 'Intensity (arb. units)' )
        
        if self.phd_checkbox_legend.IsChecked():
            self.phd_fig.axes.legend( loc=self.phd_choice_legend_loc.GetSelection()+1 )

        self.phd_fig.canvas.draw()
        
       

    def spe_update_plot( self, just_dropped=0 ):
        """ Update plot. """
        xlim = self.spe_fig.axes.get_xlim()
        ylim = self.spe_fig.axes.get_ylim()

                
        if just_dropped>0 and not self.spe_autoscale_on_drop:
            self.spe_fig.axes.set_autoscale_on( False )
            for i in range( just_dropped ):
                line = self.spe_line_list[-(i+1)]
                spectrum = line['spectrum']
                if self.spe_normalize: spectrum.normalize()
                if self.spe_countspersecond: spectrum.counts_per_second()
                spectrum.plot( color=[c/255.0 for c in line['color']],
                    label=line['label'],
                    semilogy=self.spe_semilog,
                    as_raman=self.spe_raman,
                    yoffset = float(line['offset']) )
        else:
            self.spe_fig.axes.cla()
            self.spe_fig.axes.set_autoscale_on( True )

            for line in self.spe_line_list:
                spectrum = line['spectrum']
                if line['bg_row'] is not None:
                    spectrum.background_correct( self.spe_bg_list[line['bg_row']] )
                    
                if self.spe_normalize: spectrum.normalize()
                if self.spe_countspersecond: spectrum.counts_per_second()
                if self.spe_raman and (spectrum.laser in [None, 0.0]):
                    continue

                spectrum.plot( color=[c/255.0 for c in line['color']],
                    label=line['label'],
                    semilogy=self.spe_semilog,
                    as_raman=self.spe_raman,
                    connect_on_close=False,
                    yoffset = float(line['offset']) )
            
            if self.spe_raman:
                self.spe_fig.axes.set_xlabel( 'Wavenumbers (cm$^{-1}$)' )
            else:
                self.spe_fig.axes.set_xlabel( 'Wavelength (nm)' )
            self.spe_fig.axes.set_ylabel( 'Intensity (arb. units)' )
        
        if self.spe_checkbox_legend.IsChecked():
            self.spe_fig.axes.legend( loc=self.spe_choice_legend_loc.GetSelection()+1 )

        self.spe_fig.canvas.draw()

        
class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj, parent=None):
        wx.FileDropTarget.__init__(self)
        self.obj = obj
        self.parent = parent
        # these colors are rgb tuples, with 255 as max
        self.color_list = [ (0, 0, 255),
                            (0, 125, 0),
                            (255, 0, 0),
                            (0, 190, 190),
                            (190, 0, 190),
                            (190, 190, 0),
                            (0, 0, 0) ]

    def add_phd_files( self, filenames ):
        """ Add files to the list. """
        self.parent.notebook.SetSelection(0)
        for fname in filenames:
            self.parent.phd_grid.AppendRows(1)
            new_row = self.parent.phd_grid.GetNumberRows()-1
            directory, basename = os.path.split( fname )
            if self.parent.default_path is None:
                self.parent.default_path = directory
            label = os.path.splitext( basename )[0]
            self.parent.phd_grid.SetCellValue( new_row, self.parent.phd_label_column, label )
            if self.parent.phd_offset_all:
                offset = self.parent.phd_offset
            else:
                offset = 0.0
            self.parent.phd_grid.SetCellValue( new_row, self.parent.phd_offset_column, str(offset) )
            trace = pq.Trace( fname )
            trace.set_axes( axes=self.parent.phd_fig.axes )
            self.parent.phd_line_list.append( 
                dict( fname=fname,
                      row=new_row, 
                      color=self.color_list[ pylab.mod(new_row, len(self.color_list)) ],
                      label=label,
                      offset=offset,
                      trace=trace ) )
            self.parent.phd_grid.SetCellBackgroundColour( new_row, self.parent.phd_color_column, 
                        self.color_list[ pylab.mod(new_row, len(self.color_list)) ] )

        self.parent.phd_update_plot( just_dropped=len(filenames) ) 

        self.parent.phd_grid.FitInside()
        self.parent.phd_panel.Layout()
        self.parent.Refresh()

    def add_spe_files( self, filenames ):
        """ Add files to the list. """
        self.parent.notebook.SetSelection(1)
        for fname in filenames:
            self.parent.spe_grid.AppendRows(1)
            new_row = self.parent.spe_grid.GetNumberRows()-1
            label   = os.path.splitext( os.path.basename( fname ) )[0]
            offset  = 0.0 if not self.parent.spe_checkbox_offset.IsChecked() else new_row*self.parent.spe_offset
            s       = winspec.Spectrum( fname )
            if new_row == 0 or self.parent.spe_grid.GetCellValue( new_row-1, self.parent.spe_laser_column ) == "":
                s.laser = None
            else:
                s.laser = float(self.parent.spe_grid.GetCellValue( new_row-1, self.parent.spe_laser_column ))
            self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_label_column, label )
            self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_offset_column, str(offset) )
            if s.laser is None:
                self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_laser_column, "" )
            else:
                self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_laser_column, "{0:.1f}".format(s.laser) )

            if s.background_corrected:
                self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_bg_column, 'y' )
                bg_row = None
            elif len( self.parent.spe_bg_list ) > 0:
                # default BG file will be the last one added
                bg_row = self.parent.spe_grid_bg.GetNumberRows()-1
                self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_bg_column, str(bg_row+1) )
            else:
                self.parent.spe_grid.SetCellValue( new_row, self.parent.spe_bg_column, 'n' )
                bg_row = None

                
                
            s.set_axes( axes=self.parent.spe_fig.axes )
            self.parent.spe_grid.SetReadOnly( new_row, self.parent.spe_bg_column )
            self.parent.spe_line_list.append( 
                dict( fname=fname,
                      row=new_row, 
                      color=self.color_list[ pylab.mod(new_row, len(self.color_list)) ],
                      label=label,
                      bg_row=bg_row,
                      spectrum=s,
                      offset=offset) )
            
            self.parent.spe_grid.SetCellBackgroundColour( new_row, self.parent.spe_color_column, 
                        self.color_list[ pylab.mod(new_row, len(self.color_list)) ] )
    
        self.parent.spe_update_plot( just_dropped=len(filenames) ) 

        self.parent.spe_grid.FitInside()
        self.parent.spe_panel.Layout()
        self.parent.Refresh()
        

    def OnDropFiles(self, x, y, filenames):
        """ Drop Event handler. """
        phdfiles = [ fname for fname in filenames if ".phd" in fname ]
        #spefiles = [ fname for fname in filenames if ".SPE" in fname ]
        spefiles = [ fname for fname in filenames if ".SPE" in fname or ".txt" in fname ]
        if len(spefiles) > 0: self.add_spe_files( spefiles )
        if len(phdfiles) > 0: self.add_phd_files( phdfiles )


class LifetimeFitFrame( HuPlot_GUI.LifetimeFitFrame ):
    def __init__( self, parent ):
        HuPlot_GUI.LifetimeFitFrame.__init__( self, parent )
        self.current_row = parent.current_row
        self.phd_line_list = parent.phd_line_list
        self.parent = parent
        self.phd_fig_ylim = self.parent.phd_fig.axes.get_ylim()
        self.parent.spe_fig.axes.set_autoscale_on( False )
        self.col_t = 0
        self.col_amp = 1
        self.col_offset = 2
        self.parent.lifetime_fit_frame_open = True

        self.trace = self.phd_line_list[self.current_row]['trace']
        if self.trace.has_fit:
            self.fitstart = self.trace.fitstart
            x, self.trace_max = self.trace.get_max()
            if 'l2' in self.trace.fitresults.keys():
                numexp = 3
            elif 'l1' in self.trace.fitresults.keys():
                numexp = 2
            else:
                numexp = 1
            self.phdfit_choice_number_exponentials.SetSelection( numexp-1 )
            self.update_fitparams_grid()
        else:
            self.fitstart, self.trace_max = self.trace.get_max()
            self.phdfit_fitparams_grid.SetCellValue( 0, self.col_amp, "%.3f" %  self.trace_max )
            self.phdfit_fitparams_grid.SetCellValue( 0, self.col_t, "5.0" )
            self.phdfit_fitparams_grid.SetCellValue( 0, self.col_offset, "0.0" )
            self.trace.set_axes( axes=self.parent.phd_fig.axes )
            self.fit_trace()

        self.update_fig_background()
        directory, fname = os.path.split( self.phd_line_list[self.current_row]['fname'] )
        self.phdfit_fname.SetLabel( fname )
        self.phdfit_directory.SetLabel( directory )

        self.phdfit_txtctrl_fitstart.SetValue( str(self.fitstart) )
        self.phdfit_slider_fitstart.SetValue( 1000*self.fitstart )
        self.update_fitstart_line()

        
    def fit_trace( self ):
        """ Fit. """
        guess_l0 = float( self.phdfit_fitparams_grid.GetCellValue( 0, self.col_t ) )
        guess_a0 = float( self.phdfit_fitparams_grid.GetCellValue( 0, self.col_amp ) )
        guess_b = float( self.phdfit_fitparams_grid.GetCellValue( 0, self.col_offset ) )
        guess = dict( l0=guess_l0, a0=guess_a0, b=guess_b )

        if self.phdfit_choice_number_exponentials.GetSelection() > 0:
            l1 = self.phdfit_fitparams_grid.GetCellValue( 1, self.col_t )
            a1 = self.phdfit_fitparams_grid.GetCellValue( 1, self.col_amp )
            guess_l1 = float(l1) if l1 != "" else guess_l0*2.0
            guess_a1 = float(a1) if a1 != "" else guess_a0*0.9
            guess['l1'] = guess_l1
            guess['a1'] = guess_a1
            
        if self.phdfit_choice_number_exponentials.GetSelection() > 1:
            l2 = self.phdfit_fitparams_grid.GetCellValue( 2, self.col_t )
            a2 = self.phdfit_fitparams_grid.GetCellValue( 2, self.col_amp )
            guess_l2 = float(l2) if l2 != "" else l1*2.0
            guess_a2 = float(a2) if a2 != "" else a1*0.9
            guess['l2'] = guess_l2
            guess['a2'] = guess_a2

        self.trace.fitstart = self.fitstart
        self.trace.fit_exponential( tstart=self.fitstart, guess=guess,
            verbose=False, fixed_params=['b'] )
        if hasattr( self.trace, 'bestfit_line' ):
            self.trace.bestfit_line.set_ydata( self.trace.bestfit )
            self.trace.bestfit_line.set_xdata( self.trace.t[0][pylab.find(self.trace.t[0]>=self.trace.fitstart)] )
        else:
            self.trace.bestfit_line, = self.parent.phd_fig.axes.plot(
                self.trace.t[0][pylab.find(self.trace.t[0]>=self.fitstart)],
                self.trace.bestfit,
                '-k', scalex=False, scaley=False )
        self.parent.phd_fig.axes.set_ylim( self.phd_fig_ylim )
        self.parent.phd_fig.canvas.draw()
        self.update_fig_background()
        self.update_fitparams_grid()
        self.update_fitstart_line()

    def on_close_LifetimeFitFrame( self, event ):
        """ Event handler. """
        self.parent.phd_update_plot()
        self.Destroy()

    def on_phdfit_button_refit_clicked( self, event ):
        """ Event handler. """
        self.fit_trace()

    def on_phdfit_button_close_clicked( self, event ):
        """ Event handler. """
        self.Destroy()

    def on_phdfit_button_spinbutton_spinup( self, event ):
        """ Event handler. """
        if self.fitstart < 13.595:
            self.fitstart += 0.005
            self.phdfit_txtctrl_fitstart.SetValue( str(self.fitstart) )
            self.on_phdfit_txtctrl_fitstart_changed( None )

    def on_phdfit_button_spinbutton_spindown( self, event ):
        """ Event handler. """
        if self.fitstart > 0.0:
            self.fitstart -= 0.005
            self.phdfit_txtctrl_fitstart.SetValue( str(self.fitstart) )
            self.on_phdfit_txtctrl_fitstart_changed( None )

    def on_phdfit_choice_numexp_changed( self, event ):
        """ Event handler. """
        if self.phdfit_choice_number_exponentials.GetSelection() == 0:
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_amp, "" )
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_t, "" )
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_offset, "" )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_amp, "" )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_t, "" )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_offset, "" )

        if self.phdfit_choice_number_exponentials.GetSelection() == 1:
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_amp, "%.3f" %  (self.trace_max/5.0) )
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_t, "10.0" )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_amp, "" )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_t, "" )

        if self.phdfit_choice_number_exponentials.GetSelection() > 1:
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_amp, "%.3f" %  (self.trace_max/10.0) )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_t, "20.0" )

        self.fit_trace()
        self.update_fitstart_line()

    def on_phdfit_txtctrl_fitstart_changed( self, event ):
        """ Event handler. """
        try:
            self.fitstart = float( self.phdfit_txtctrl_fitstart.GetValue() )
        except ValueError:
            return True
        
        self.phdfit_slider_fitstart.SetValue( 1000*self.fitstart )
        #self.fit_trace()
        self.update_fitstart_line()
        
    def on_phdfit_slider_fitstart_changed( self, event ):
        """ Event handler. """
        self.fitstart = float(self.phdfit_slider_fitstart.GetValue())/1000.0
        self.phdfit_txtctrl_fitstart.SetValue( str(self.fitstart) )
        self.update_fitstart_line()

    def update_fitparams_grid( self ):
        """ Update fitparams display """
        if not self.trace.has_fit: return True
        
        self.phdfit_fitparams_grid.SetCellValue( 0, self.col_t, "%.3f" % self.trace.fitresults['l0'] )
        self.phdfit_fitparams_grid.SetCellValue( 0, self.col_amp, "%.3f" % self.trace.fitresults['a0'] )
        self.phdfit_fitparams_grid.SetCellValue( 0, self.col_offset, "%.3f" % self.trace.fitresults['b'] )
        if self.phdfit_choice_number_exponentials.GetSelection() > 0:
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_t, "%.3f" % self.trace.fitresults['l1'] )
            self.phdfit_fitparams_grid.SetCellValue( 1, self.col_amp, "%.3f" % self.trace.fitresults['a1'] )
        if self.phdfit_choice_number_exponentials.GetSelection() > 1:
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_t, "%.3f" % self.trace.fitresults['l2'] )
            self.phdfit_fitparams_grid.SetCellValue( 2, self.col_amp, "%.3f" % self.trace.fitresults['a2'] )
    
    def update_fitstart_line( self ):
        """ Update line position. """
        self.parent.phd_fig.canvas.restore_region( self.phd_fig_bg )
        self.fitstart_line.set_xdata( [self.fitstart]*2 )
        self.parent.phd_fig.axes.draw_artist( self.fitstart_line )
        self.parent.phd_fig.canvas.blit( self.parent.phd_fig.axes.bbox )

    def update_fig_background( self ):
        """ Refresh the 'figure background'. """
        self.fitstart_line, = self.parent.phd_fig.axes.plot(
                [self.fitstart]*2,
                self.parent.phd_fig.axes.get_ylim(),
                '--k', animated=True )
        self.phd_fig_bg = self.parent.phd_fig.canvas.copy_from_bbox( self.parent.phd_fig.axes.bbox )
        

class SPEFitFrame( HuPlot_GUI.SPEFitFrame ):
    """ Window for setting and adjusting parameters
    for fitting Lorentzian functions to SPE spectra. """
    def __init__( self, parent ):
        HuPlot_GUI.SPEFitFrame.__init__( self, parent )

        self.row_label_column = parent.row_label_column
        self.current_row      = parent.current_row
        self.spe_line_list    = parent.spe_line_list
        self.parent           = parent
        self.col_x0           = 0
        self.col_ymax         = 1
        self.col_Q            = 2
        self.col_offset       = 3
        self.num_lorentzians  = 1
        self.axes             = self.parent.spe_fig.axes
        self.spe_fig_ylim     = self.axes.get_ylim()
        self.spectrum         = self.spe_line_list[self.current_row]['spectrum']
        self.parent.spe_fit_frame_open = True

        """ Set initial fit range, the minimum of the xaxis range and the wavelength data """
        xmin, xmax = self.axes.get_xlim()
        if xmin < self.spectrum.wavelen[0]: xmin = self.spectrum.wavelen[0]
        if xmax > self.spectrum.wavelen[-1]: xmax = self.spectrum.wavelen[-1]
        self.fitrange = (xmin, xmax)
        self.spefit_txtctrl_fitstart.SetValue( "{0:.3f}".format(xmin) )
        self.spefit_txtctrl_fitend.SetValue( "{0:.3f}".format(xmax) )

        parent.spe_fig.canvas.mpl_connect( 'button_press_event', self.on_click_press_in_spe_fig )
        self.initialize_row(0)

    def initialize_row( self, row ):
        """ Set grid to default initial conditions for the fit. """
        imin, imax = self.spectrum.get_fitrange_indices(self.fitrange) 
        self.grid.SetCellValue( row, self.col_x0,
            "%.3f" % self.spectrum.wavelen[imin+self.spectrum.lum[imin:imax].argmax()] )
        self.grid.SetCellValue( row, self.col_ymax, "None" )
        self.grid.SetCellValue( row, self.col_Q, "1000" )
        self.grid.SetCellValue( row, self.col_offset, "None" )


    def on_click_press_in_spe_fig( self, event ):
        """ Event handler. """
        if not event.inaxes: return True
        num_selected_rows = len(self.grid.GetSelectedRows())
        if num_selected_rows == 0 or num_selected_rows > 1:
            return True
        
        current_row = self.grid.GetSelectedRows()[0]
        if current_row > self.choice_numlorentzians.GetSelection():
            return True
        
        x = event.xdata
        self.grid.SetCellValue( current_row, self.col_x0, "%.3f" % x )

        self.statusbar.SetStatusText("")
        

    def on_close_SPEFitFrame( self, event ):
        """ Event handler. """
        self.parent.spe_update_plot()
        self.Destroy()

    def on_choice_numlorentzians_changed( self, event ):
        """ Event handler.
        TODO: Fix it so it stops re-initializing the last row when you
        downsize (e.g. from 3-2 it deletes 3 as it should but reinitializes 2...?)
        """
        if self.choice_numlorentzians.GetSelection()+1 > self.num_lorentzians:
            # add row(s) to grid
            for i in range(event.GetSelection()+1 - self.num_lorentzians):
                self.grid.AppendRows(1)
                new_row = self.grid.GetNumberRows()-1
                self.initialize_row( new_row )
        elif self.choice_numlorentzians.GetSelection()+1 < self.num_lorentzians:
            # remove row(s) from grid
            self.grid.DeleteRows(
                pos=self.choice_numlorentzians.GetSelection(),
                numRows= self.num_lorentzians-(self.choice_numlorentzians.GetSelection()+1) )
        else:
            # no change
            return False
        
        self.num_lorentzians = self.choice_numlorentzians.GetSelection()+1
        self.grid.FitInside()
        self.panel.Layout()
        self.Refresh()
    
    def on_spefit_button_fit_clicked( self, event ):
        """ Event handler. """
        self.num_lorentzians = self.choice_numlorentzians.GetSelection()+1
        if self.checkbox_level.IsChecked():
            self.spectrum.remove_linear_background(
                while_fitting=True,
                npoints=int(self.spefit_combo_numberpoints_level.GetValue()))
        else:
            self.spectrum.leave_linear_background()
        
        imin, imax = self.spectrum.get_fitrange_indices(self.fitrange) 

        center = []
        width = []
        for i in range( self.num_lorentzians ):
            center.append( float(self.grid.GetCellValue( i, self.col_x0 )) )
            width.append( center[i]/float(self.grid.GetCellValue( i, self.col_Q )) )

        try:
            self.spectrum.fit_lorentzians( 
                center=center, 
                width=width, 
                fitrange=(imin,imax),
                plotfit=False, 
                printparams=True )
        except RuntimeError:
            print "Fit failed."
            return False

        xfit        = np.linspace(self.fitrange[0], self.fitrange[1], 1000)
        best_params = kasey_fitspectra.params_to_lists( self.spectrum.fit_params )
        yfit        = kasey_fitspectra.lorentzians(xfit, *best_params)

        if self.checkbox_level.IsChecked():
            yoffset = np.polyval( self.spectrum.fit_params[0]['slope_fit'], xfit )
            yfit   += yoffset
        else:
            yoffset = best_params[0]            

            
        if hasattr( self.spectrum, 'bestfit_line' ):
            self.spectrum.bestfit_line.set_xdata( xfit )
            self.spectrum.bestfit_line.set_ydata( yfit )
        else:
            self.spectrum.bestfit_line, = self.axes.plot( xfit, yfit, "-", color="black")
        self.axes.figure.canvas.draw()
        
        for i, p in enumerate(self.spectrum.fit_params):
            if False: #len(self.spectrum.fit_params) > 1:
                """ Plot each peak individually, too. """
                single_peak_params = kasey_fitspectra.params_to_lists( [p] )
                single_peak_params[0] = yoffset
                yfit_peak = kasey_fitspectra.lorentzians(xfit, *single_peak_params)
                self.axes.plot( xfit, yfit_peak, '-', color='black' )
                p['xfit'] = xfit
                p['yfit'] = yfit_peak
                p['yfit_all'] = yfit

            self.grid.SetCellValue( i, self.col_x0, "{0:.3f}".format(p['x0']) )
            self.grid.SetCellValue( i, self.col_ymax, "{0:.3f}".format(p['ymax']) )
            self.grid.SetCellValue( i, self.col_Q, "{0:.1f}".format(p['Q']) )
            self.grid.SetCellValue( i, self.col_offset, "{0:.3f}".format(p['yoffset']) )
        

    def on_spefit_button_close_clicked( self, event ):
        """ Event handler. """
        self.Destroy()

    def on_grid_label_leftclick( self, event ):
        """ Event handler. """
        self.statusbar.SetStatusText("Click on peak to set initial conditions.")
        event.Skip()

    def on_spefit_grid_label_rightclick( self, event ):
        """ Event handler. """
        if len(self.grid.GetSelectedRows()) > 1:
            pass
            
        elif event.GetCol() == self.row_label_column:
            if not hasattr(self, "popup_fitrow"):
                self.popup_fit_start = wx.NewId()
     
            self.current_row = event.GetRow()

            menu = wx.Menu()
            fit_start = wx.MenuItem( menu, self.popup_fit_start, "Set Center" )
            menu.AppendItem( fit_start )
            wx.EVT_MENU( self, self.popup_fit_start, self.spefit_change_start )
            
            self.PopupMenu(menu)
            menu.Destroy()

    def spefit_change_start( self, event ):
        pass

class SPEFit_SliderFrame( HuPlot_GUI.SPEFit_SliderFrame ):
    """ Window for adjusting the initial condition for the peak location. """
    def __init__( self, parent ):
        HuPlot_GUI.SPEFit_SliderFrame.__init__( self, parent )

        pass
        
    def on_spefit_popup_slider_scrolled( self, event ):
        pass
        
    def on_spefit_popup_button_okay_clicked( self, event ):
        pass
        
    def on_spefit_popup_button_cancel_clicked( self, event ):
        """ Cancel reset of fit. """
        self.Destroy()        

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()

