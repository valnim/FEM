classdef TimeStamp
    %TIMESTAMP A simple class we will use for time stepping. Note that we
    %only perform quasistatic computations
    
    properties ( SetAccess = private )
        index
        time
    end
    
    methods
        function self = TimeStamp( index, time )
            self.index = index;
            self.time = time;
        end
    end    
end

