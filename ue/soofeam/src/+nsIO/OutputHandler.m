classdef ( Abstract ) OutputHandler < handle
    %OUTPUTHANDLER 
    
    properties ( SetAccess = private )
        file_name
        current_time_step = -1;
    end
    
    methods
        function self = OutputHandler( file_name )
            self.file_name = file_name;
            
            % delete all previous files in the current directory
            del_files = [file_name,'.vtk.*'];
            delete(del_files);
        end
        
        function write( self, model )
            self.current_time_step = self.current_time_step + 1;
            
            current_file_path = [self.file_name,'.vtk.',num2str(self.current_time_step)];
            current_folder_path = fileparts(current_file_path);
            
            if exist(current_folder_path,'dir') == 7
            else
                mkdir (current_folder_path);
            end
            
            file_id = fopen(current_file_path,'w');

            % write output to file
            self.writeResults( model, file_id );
            
            fclose(file_id);
        end
    end
    
    methods ( Static, Abstract, Access = protected )
        writeResults ( model, file_id )
    end
end

