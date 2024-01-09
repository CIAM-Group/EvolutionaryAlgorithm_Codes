function para = RBFCreate(ax, ay, kernel)
[N, D] = size(ax);
% % Normlization
% %%%%%%*****************************
% xmin = min(ax, [], 1);
% xmax = max(ax, [], 1);
% ymin = min(ay, [], 1);
% ymax = max(ay, [], 1);
% ax = 2./(repmat(xmax - xmin, N, 1)) .* (ax - repmat(xmin, N, 1)) - 1;
% ay = 2./(repmat(ymax - ymin, N, 1)) .* (ay - repmat(ymin, N, 1)) - 1;
% 
% for i = 1 : length(xmin)
%    if xmin(i) ~= xmax(i)
%        ax(:, i) = 2 ./ (repmat(xmax(i) - xmin(i), N, 1)) .* (ax(:, i) - repmat(xmin(i), N, 1)) - 1;
%    end
% end
% 
% for i = 1 : length(ymin)
%    if ymin(i) ~= ymax(i)
%        ay(:, i) = 2./(repmat(ymax(i) - ymin(i), N, 1)) .* (ay(:, i) - repmat(ymin(i), N, 1)) - 1;
%    end
% end

r = dist(ax, ax');
switch kernel
    case 'gaussian'
        Phi = radbas(sqrt(-log(.5))*r);
    case 'cubic'
        Phi = r.^3;
    case 'multiquadric'
        Phi=sqrt(r.^2+0.8^2);
end
P = [ones(N, 1), ax];
A = [Phi, P; P' zeros(D + 1, D + 1)];
b = [ay; zeros(D + 1, size(ay, 2))];


 theta = A \ b;
%theta = pinv(A)*b;

para.alpha = theta(1 : N, :);       %for radial basis function
para.beta = theta(N + 1 : end, :);  % for polynomial function

% para.xmin = xmin;
% para.xmax = xmax;
% para.ymin = ymin;
% para.ymax = ymax;
para.nodes = ax;    % normlization
para.kernel = kernel;
para.Phi = Phi;
end