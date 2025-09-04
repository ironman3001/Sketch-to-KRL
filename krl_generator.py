class KRLGenerator:
    """
    Class for generating KUKA Robot Language (KRL) code from paths
    """
    
    def __init__(self, program_name="PATH_PROGRAM"):
        """
        Initialize the KRL generator
        
        Args:
            program_name: Name of the KRL program
        """
        self.program_name = program_name
        self.points = []
    
    def generate_src_code(self, paths, start_position, motion_types, use_coordinates=False):
        """
        Generate KRL source code (.src file)
        
        Args:
            paths: List of paths as coordinate points
            start_position: Starting position ("HOME" or "Anywhere")
            motion_types: List of motion types to use (LIN, PTP, CIRC, SPLINE)
            use_coordinates: Whether to use exact coordinates from the sketch
            
        Returns:
            src_code: Generated KRL source code
        """
        # Start with the program header
        src_code = f"DEF {self.program_name}()\n"
        src_code += "   BAS (#INITMOV,0)\n"
        
        # Add start position
        if start_position == "HOME":
            src_code += "   PTP HOME\n"
        else:
            src_code += "   PTP P0\n"
        
        # Reset points list
        self.points = []
        
        # Generate motion commands based on extracted paths
        point_index = 1
        
        for path_idx, path in enumerate(paths):
            if not path:
                continue
                
            # Skip paths that are too short
            if len(path) < 3:
                continue
            
            # Distribute motion types along the path
            if not motion_types:
                motion_types = ["LIN"]  # Default to LIN if none selected
            
            # Process points in the path
            i = 0
            while i < len(path):
                motion_type = motion_types[i % len(motion_types)]
                
                # Store the point for DAT file generation
                self.points.append(path[i])
                
                if motion_type == "CIRC" and i < len(path) - 2:
                    # CIRC requires two points: auxiliary and end point
                    aux_point = path[i + 1]
                    end_point = path[i + 2]
                    
                    # Store the auxiliary point
                    self.points.append(aux_point)
                    
                    src_code += f"   CIRC P{point_index}, P{point_index + 1}\n"
                    point_index += 2
                    i += 3  # Skip the next two points as they're used for the CIRC
                
                elif motion_type == "SPLINE" and i < len(path) - 3:
                    # Start SPLINE block
                    src_code += "   SPLINE\n"
                    
                    # Add SPL points
                    spline_points = min(4, len(path) - i)
                    for j in range(spline_points):
                        # Store the point
                        if i + j < len(path):
                            self.points.append(path[i + j])
                            src_code += f"      SPL P{point_index}\n"
                            point_index += 1
                    
                    # End SPLINE block
                    src_code += "   ENDSPLINE\n"
                    i += spline_points  # Skip points used in the SPLINE
                
                else:
                    # LIN or PTP
                    src_code += f"   {motion_type} P{point_index}\n"
                    point_index += 1
                    i += 1
        
        # Return to home position
        src_code += "   PTP HOME\n"
        
        # End program
        src_code += "END\n"
        
        return src_code
    
    def generate_dat_code(self, use_coordinates=False):
        """
        Generate KRL data file (.dat file)
        
        Args:
            use_coordinates: Whether to use exact coordinates from the sketch
            
        Returns:
            dat_code: Generated KRL data code
        """
        # Generate DAT file header
        dat_code = f"&ACCESS RVP\n&REL 1\n&PARAM TEMPLATE = C_PTP\n&PARAM EDITMASK = *\nDEFDAT {self.program_name}\n\n"
        dat_code += "DECL E6POS XHOME={X 0.0,Y 0.0,Z 0.0,A 0.0,B 0.0,C 0.0}\n"
        
        # Add point definitions
        for i, point in enumerate(self.points):
            x, y = point
            
            # Scale coordinates to a reasonable robot workspace (mm)
            # Assuming the sketch is in pixel coordinates
            x_scaled = (x / 500) * 1000  # Scale to 0-1000mm range
            y_scaled = (y / 500) * 1000
            z = 100  # Fixed Z height for simplicity
            
            # Add some variation to Z for visual interest
            if i % 3 == 0:
                z = 120
            elif i % 3 == 1:
                z = 100
            else:
                z = 80
            
            dat_code += f"DECL E6POS P{i+1}={{X {x_scaled:.1f},Y {y_scaled:.1f},Z {z:.1f},A 0.0,B 90.0,C 0.0}}\n"
        
        dat_code += "ENDDAT\n"
        
        return dat_code