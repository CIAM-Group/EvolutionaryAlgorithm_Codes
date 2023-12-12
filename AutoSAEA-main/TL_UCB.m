function [U_value] = TL_UCB(sum_reward, id, q_value, apha)

         U_value = q_value + sqrt((apha*log(id))/length(sum_reward));
end