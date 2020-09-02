import xml.etree.ElementTree as ET

import numpy as np

from scipy.integrate import quad

class _Geometry():
    """ the _Geometry describes the geometry entry of open drive
        
        Parameters
        ----------
            s (float): the start s value (along road) of the geometry
               
            x (float): start x coordinate of the geometry
                
            y (float):  start y coordinate of the geometry
                
            heading (float): heading of the geometry

            geom_type (Line, Sprial,ParamPoly3, or Arc): the type of geometry

        Attributes
        ----------
            s (float): the start s value (along road) of the geometry
               
            x (float): start x coordinate of the geometry
                
            y (float):  start y coordinate of the geometry
                
            heading (float): heading of the geometry

            geom_type (Line, Sprial,ParamPoly3, or Arc): the type of geometry

        Methods
        -------
            get_element()
                Returns the full ElementTree of the class

            get_attributes()
                Returns a dictionary of all attributes of the class
    """

    def __init__(self,s,x,y,heading,geom_type):
        """ initalizes the PlanView

        Parameters
        ----------
            s (float): the start s value (along road) of the geometry
               
            x (float): start x coordinate of the geometry
                
            y (float):  start y coordinate of the geometry
                
            heading (float): heading of the geometry

            geom_type (Line, Sprial,ParamPoly3, or Arc): the type of geometry

        """ 
        self.s = s
        self.x = x
        self.y = y
        self.heading = heading
        self.geom_type = geom_type
        _,_,_,self.length = self.geom_type.get_end_data(self.x,self.y,self.heading)

    def get_end_data(self):
        return self.geom_type.get_end_data(self.x,self.y,self.heading)
        
    def get_attributes(self):
        """ returns the attributes of the _Geometry as a dict

        """
        retdict = {}
        retdict['s'] = str(self.s)
        retdict['x'] = str(self.x)
        retdict['y'] = str(self.y)
        retdict['hdg'] = str(self.heading)
        retdict['length'] = str(self.length)
        return retdict


    def get_element(self):
        """ returns the elementTree of the _Geometry

        """
        element = ET.Element('geometry',attrib=self.get_attributes())
        element.append(self.geom_type.get_element())
        return element



class PlanView():
    """ the PlanView is the geometrical description of a road, 
        
        Parameters
        ----------
            x_start (float): start x coordinate of the first geometry
                Default: 0

            y_start (float): start y coordinate of the first geometry
                Default: 0

            h_start (float): starting heading of the first geometry
                Default: 0

        Attributes
        ----------
            present_x (float): the start x coordinate of the next geometry added

            present_y (float): the y coordinate of the next geometry added

            present_h (float): the heading coordinate of the next geometry added

            present_s (float): the along road measure of the next geometry added

        Methods
        -------
            get_element(elementname)
                Returns the full ElementTree of the class

            get_total_length()
                Returns the full length of the PlanView

            add_geometry(geom,lenght)
                adds a new geometry entry to the planeview

    """
    def __init__(self,x_start=0,y_start=0,h_start=0):
        """ initalizes the PlanView

        Parameters
        ----------
            x_start (float): start x coordinate of the first geometry
                Default: 0

            y_start (float): start y coordinate of the first geometry
                Default: 0

            h_start (float): starting heading of the first geometry
                Default: 0

        """ 
        self.present_x = x_start
        self.present_y = y_start
        self.present_h = h_start
        self.present_s = 0

        self._geometries = []

    def add_geometry(self,geom,heading = None):
        """ add_geometry adds a geometry to the planview and calculates
        
        Parameters
        ----------
            geom (Line, Sprial, ParamPoly3, or Arc): the type of geometry

            heading (float): override the previous heading (optional), this will create an ugly road :)

        """
        if heading:
            self.present_h = heading
        newgeom = _Geometry(self.present_s,self.present_x,self.present_y,self.present_h,geom)

        self.present_x, self.present_y, self.present_h, length = newgeom.get_end_data()
        self.present_s += length
        
        self._geometries.append(newgeom)

    def get_total_length(self):
        """ returns the total length of the planView

        """
        return self.present_s
    def get_element(self):
        """ returns the elementTree of the WorldPostion

        """
        element = ET.Element('planView')
        for geom in self._geometries:
            element.append(geom.get_element())
        return element




class Line():
    """ the line class creates a line type of geometry

        Parameters
        ----------
            length (float): length of the line

        Attributes
        ----------
            length (float): length of the line

        Methods
        -------
            get_element(elementname)
                Returns the full ElementTree of the class

            get_end_data(x,y,h)
                Returns the end point of the geometry

    """
    def __init__(self,length):
        self.length = length

    def get_end_data(self,x,y,h):
        """ Returns the end point of the geometry
        
        Parameters
        ----------
            x (float): x start point of the geometry

            y (float): y start point of the geometry

            h (float): start heading of the geometry

        Returns
        ----------
            x (float): the final x point

            y (float): the final y point

            h (float): the final heading

            length (float): length of the road

        """

        new_x = self.length*np.cos(h) + x
        new_y = self.length*np.sin(h) + y
        new_h = h

        return new_x, new_y, new_h, self.length
    
    def get_element(self):
        """ returns the elementTree of the WorldPostion

        """
        element = ET.Element('line')
        
        return element
        


class Sprial():
    """ the Spiral (Clothoid) creates a spiral type of geometry
        
        Parameters
        ----------
            curvstart (float): starting curvature of the Spiral

            curvend (float): final curvature of the Spiral

            
        Attributes
        ----------
            curvstart (float): starting curvature of the Spiral

            curvend (float): final curvature of the Spiral

        Methods
        -------
            get_element()
                Returns the full ElementTree of the class

            get_attributes()
                Returns a dictionary of all attributes of the class

            get_end_data(length,x,y,h)
                Returns the end point of the geometry        
    """
    def __init__(self,curvstart,curvend):
        """ initalizes the Line

        Parameters
        ----------
            curvstart (float): starting curvature of the Spiral

            curvend (float): final curvature of the Spiral
        """ 
        self.curvstart = curvstart
        self.curvend = curvend

    def get_end_data(self,length,x,y,h):
        """ Returns the end point of the geometry
        
        Parameters
        ----------
            length (float): length of the geometry

            x (float): x start point of the geometry

            y (float): y start point of the geometry

            h (float): start heading of the geometry

        Returns
        ---------

            x (float): the final x point
            y (float): the final y point
            h (float): the final heading
        """

        pass
        # TODO: fix this stuffs...

    def get_attributes(self):
        """ returns the attributes of the Line as a dict

        """
        return {'curvStart': str(self.curvstart), 'curvEnd': str(self.curvend)}

    def get_element(self):
        """ returns the elementTree of the Line

        """
        element = ET.Element('spiral',attrib=self.get_attributes())
        
        return element
        

class Arc():
    """ the Arc creates a arc type of geometry
        
        Parameters
        ----------
            curvature (float): curvature of the arc

            length (float): length of the arc (optional or use angle)

            angle (float): angle of the arc (optional or use length)

        Attributes
        ----------
            curvature (float): curvature of the arc

            length (float): length of the arc 

            angle (float): angle of the arc

        Methods
        -------
            get_element()
                Returns the full ElementTree of the class

            get_attributes()
                Returns a dictionary of all attributes of the class

            get_end_data(x,y,h)
                Returns the end point of the geometry
    """
    def __init__(self,curvature,length = None, angle=None):
        """ initalizes the Arc

        Parameters
        ----------
            curvature (float): curvature of the arc

            length (float): length of the arc (optional or use angle)

            angle (float): angle of the arc (optional or use length)

        """

        if length == None and angle == None:
            raise ValueError('neither length nor angle defined, for arc')
        
        if length != None and angle != None:
            raise ValueError('both length and angle set, only one is requiered')

        self.length = length
        self.angle = angle
        if curvature == 0:
            raise ValueError('You are creating a straight line, please use Line instead')
        self.curvature = curvature

    def get_end_data(self,x,y,h):
        """ Returns information about the end point of the geometry
        
        Parameters
        ----------
            x (float): x start point of the geometry

            y (float): y start point of the geometry

            h (float): start heading of the geometry

        Returns
        ---------
            
            x (float): the final x point

            y (float): the final y point

            h (float): the final heading

            length (float): length of the element

        """
        radius = 1/np.abs(self.curvature)
        if self.curvature < 0:
            phi_0 = h + np.pi/2
            x_0 = x - np.cos(phi_0)*radius
            y_0 = y - np.sin(phi_0)*radius

        else:
            phi_0 = h - np.pi/2
            x_0 = x - np.cos(phi_0)*radius
            y_0 = y - np.sin(phi_0)*radius

        if self.length:
            self.angle = self.length * self.curvature

        new_ang = self.angle + phi_0
        if self.angle:         
            self.length = np.abs(radius*self.angle)

            
        

        new_h = h + self.angle
        new_x = np.cos(new_ang)*radius + x_0
        new_y = np.sin(new_ang)*radius + y_0

        return new_x, new_y, new_h, self.length

    def get_attributes(self):
        """ returns the attributes of the Arc as a dict

        """
        return {'curvature': str(self.curvature)}

    def get_element(self):
        """ returns the elementTree of the Arc

        """
        element = ET.Element('arc',attrib=self.get_attributes())
        
        return element



class ParamPoly3():
    """ the ParamPoly3 class creates a parampoly3 type of geometry, in the coordinate systeme U (along road), V (normal to the road)
        
        the polynomials are on the form
        uv(p) = a + b*p + c*p^2 + d*p^3

        Parameters
        ----------
            au (float): coefficient a of the u polynomial
            
            bu (float): coefficient b of the u polynomial

            cu (float): coefficient c of the u polynomial

            du (float): coefficient d of the u polynomial

            av (float): coefficient a of the v polynomial

            bv (float): coefficient b of the v polynomial

            cv (float): coefficient c of the v polynomial

            dv (float): coefficient d of the v polynomial

            prange (str): "normalized" or "arcLength"
                Default: "normalized"

            length (float): total length of arc, used if prange == arcLength

        Attributes
        ----------
            au (float): coefficient a of the u polynomial
            
            bu (float): coefficient b of the u polynomial

            cu (float): coefficient c of the u polynomial

            du (float): coefficient d of the u polynomial

            av (float): coefficient a of the v polynomial

            bv (float): coefficient b of the v polynomial

            cv (float): coefficient c of the v polynomial

            dv (float): coefficient d of the v polynomial
           
            prange (str): "normalized" or "arcLength"
                Default: "normalized"

            length (float): total length of arc, used if prange == arcLength

        Methods
        -------
            get_element(elementname)
                Returns the full ElementTree of the class

            get_attributes()
                Returns a dictionary of all attributes of the class

            get_end_coordinate(length,x,y,h)
                Returns the end point of the geometry
    """
    def __init__(self,au,bu,cu,du,av,bv,cv,dv,prange='normalized',length=None):
        """ initalizes the ParamPoly3

        Parameters
        ----------
            au (float): coefficient a of the u polynomial
            
            bu (float): coefficient b of the u polynomial

            cu (float): coefficient c of the u polynomial

            du (float): coefficient d of the u polynomial

            av (float): coefficient a of the v polynomial

            bv (float): coefficient b of the v polynomial

            cv (float): coefficient c of the v polynomial

            dv (float): coefficient d of the v polynomial
           
            prange (str): "normalized" or "arcLength"
                Default: "normalized"
                
            length (float): total length of arc, used if prange == arcLength
        """ 
        
        self.au = au
        self.bu = bu
        self.cu = cu
        self.du = du
        self.av = av
        self.bv = bv
        self.cv = cv
        self.dv = dv
        self.prange = prange
        if prange == 'arcLength' and length == None:
            raise ValueError('No length was provided for Arc with arcLength option')
        self.length = length

    def _integrand(self,p):
        """ integral function to calulate length of polynomial,
            #TODO: This is not tested or verified...
        """
        return np.sqrt( \
            (self.bu**2 + self.bv**2) + \
            4*(self.bu*self.cu + self.bv*self.cv)*p + \
            2*(3*self.bu*self.du + 2*self.cu**2 +3*self.bv*self.dv + 2*self.cv**2 )*p**2 + \
            12*(self.cu*self.du + self.cv*self.dv)*p**3 +\
            9*(self.du**2 + self.dv**2)*p**4 )

    def get_end_data(self,x,y,h):
        """ Returns the end point of the geometry
        
        Parameters
        ----------
            x (float): x start point of the geometry

            y (float): y start point of the geometry

            h (float): start heading of the geometry

        Returns
        ---------
            x (float): the final x point
            y (float): the final y point
            h (float): the final heading

        """
        if self.prange == 'normalized':
            p = 1
            I = quad(self._integrand,0,1)
            self.length = I[0]
        else:
            p = self.length
        newu = self.au + self.bu*p + self.cu*p**2 + self.du*p**3
        newv = self.av + self.bv*p + self.cv*p**2 + self.dv*p**3

        new_x = x + newu*np.cos(h)-np.sin(h)*newv
        new_y = y + newu*np.sin(h)+np.cos(h)*newv
        new_h = h + np.arctan2(self.bv + self.cv*p + self.dv*p**2,self.bu + self.cu*p + self.du*p**2)

        return new_x, new_y, new_h, self.length

    def get_attributes(self):
        """ returns the attributes of the ParamPoly3 as a dict

        """
        retdict = {}
        retdict['aU'] = str(self.au)
        retdict['bU'] = str(self.bu)
        retdict['cU'] = str(self.cu)
        retdict['dU'] = str(self.du)
        retdict['aV'] = str(self.av)
        retdict['bV'] = str(self.bv)
        retdict['cV'] = str(self.cv)
        retdict['dV'] = str(self.dv)
        retdict['pRange'] = self.prange
        return retdict
        

    def get_element(self):
        """ returns the elementTree of the ParamPoly3

        """
        element = ET.Element('paramPoly3',attrib=self.get_attributes())
        
        return element
