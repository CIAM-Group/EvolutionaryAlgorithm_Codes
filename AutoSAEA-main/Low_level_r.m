function [reward] = Low_level_r(ghf, hf, candidate_fit, NFEs, Arm)
         % Update the low-level arm reward
         N = length(ghf);
         ghf = reshape(ghf, 1, N);
         ghf_sum = [ghf, candidate_fit];
         [~, index] = sort(ghf_sum);
         in = find(index == (N+1));
         reward = -1/N*in + (N+1)/N;
        
         if candidate_fit == min(hf)
            disp(['Current optimal obtained by ' Arm 'arm is: ' num2str(candidate_fit) ' NFE=' num2str(NFEs)]);
         end

end