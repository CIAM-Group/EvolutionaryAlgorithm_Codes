function  [dmodel, perf] = dacefit_3(S, Y, regr, corr, theta0)
%DACEFIT Constrained non-linear least-squares fit of a given correlation
% model to the provided data set and regression model
%
% Call
%   [dmodel, perf] = dacefit(S, Y, regr, corr, theta0)
%   [dmodel, perf] = dacefit(S, Y, regr, corr, theta0, lob, upb)
%
% Input
% S, Y    : Data points (S(i,:), Y(i,:)), i = 1,...,m
% regr    : Function handle to a regression model
% corr    : Function handle to a correlation function
% theta0  : Initial guess on theta, the correlation function parameters
% lob,upb : If present, then lower and upper bounds on theta
%           Otherwise, theta0 is used for theta
%
% Output
% dmodel  : DACE model: a struct with the elements
%    regr   : function handle to the regression model
%    corr   : function handle to the correlation function
%    theta  : correlation function parameters
%    beta   : generalized least squares estimate
%    gamma  : correlation factors
%    sigma2 : maximum likelihood estimate of the process variance
%    S      : scaled design sites
%    Ssc    : scaling factors for design arguments
%    Ysc    : scaling factors for design ordinates
%    C      : Cholesky factor of correlation matrix
%    Ft     : Decorrelated regression matrix
%    G      : From QR factorization: Ft = Q*G' .
% perf    : struct with performance information. Elements
%    nv     : Number of evaluations of objective function
%    perf   : (q+2)*nv array, where q is the number of elements 
%             in theta, and the columns hold current values of
%                 [theta;  psi(theta);  type]
%             |type| = 1, 2 or 3, indicate 'start', 'explore' or 'move'
%             A negative value for type indicates an uphill step

% hbn@imm.dtu.dk  
% Last update September 3, 2002

% Check design points
[m n] = size(S);  % number of design sites and their dimension%%%%%%mΪ�����Ŀ��nΪά��
sY = size(Y);
if  min(sY) == 1%%%%%%%min(sY) ��ʾ������ά��
    Y = Y(:);   lY = max(sY);  sY = size(Y);%%%%%%%YΪ��Ӧ��lYΪ�����Ŀ
else
    lY = sY(1); 
end
if m ~= lY
  error('S and Y must have the same number of rows')
end

if  any(theta0 <= 0)
    error('theta0 must be strictly positive')
end

% Normalize data
mS = mean(S);   sS = std(S);%%%%%%%%%%%%mean��std��ʾ��Ϊÿһ�еľ�ֵ�ͱ�׼��
mY = mean(Y);   sY = std(Y);
% 02.08.27: Check for 'missing dimension'
j = find(sS == 0);
if  ~isempty(j)
    sS(j) = 1; 
end
j = find(sY == 0);
if  ~isempty(j)
    sY(j) = 1;
end
S = (S - repmat(mS,m,1)) ./ repmat(sS,m,1);%%%%%%%repmatΪ���ƾ�����������������m��1��
Y = (Y - repmat(mY,m,1)) ./ repmat(sY,m,1);

% Calculate distances D between points
mzmax = m*(m-1) / 2;        % number of non-zero distances
ij = zeros(mzmax, 2);       % initialize matrix with indices
D = zeros(mzmax, n);        % initialize matrix with distances��mzmax��������룬��������ÿһά�ȵľ���Ϊ����ͳ�Ƶ�
ll = 0;
for k = 1 : m-1
  ll = ll(end) + (1 : m-k);
  ij(ll,:) = [repmat(k, m-k, 1) (k+1 : m)']; % indices for sparse matrix��ijΪϡ�����ķ���Ԫ�ص��б���б�
  D(ll,:) = repmat(S(k,:), m-k, 1) - S(k+1:m,:); % differences between points��һ�ε�����D��1��m-1�У���һ����������m-1���㽫�ľ��룬�ڶ��ε�����m��2m-3�У�Ϊ�ڶ�������������m-2����ľ���
end
if  min(sum(abs(D),2) ) == 0
  error('Multiple design sites are not allowed')
end
% Regression matrix
F = feval(regr, S);  [mF p] = size(F);%%%%%%%%%%%%%%%%%%%%%%���ĵ����Ŀ�Ƿ�����ع�����FΪ�ع����������
if  mF ~= m, error('number of rows in  F  and  S  do not match'), end
if  p > mF,  error('least squares problem is underdetermined'), end

% parameters for objective function
par = struct('corr',corr, 'regr',regr, 'y',Y, 'F',F, ...
  'D', D, 'ij',ij, 'scS',sS);

% Determine theta
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ͨ��GA�㷨�Ż�thetaֵ������һ��������
global ppar
ppar=par;
FTT=10^3;
Xtheta=10;
for ii=1:1
%     ii
    lb=0.01;
    ub=20;
    Range=[lb,ub];
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%��ȡ��ʼthetaֵ
    bounds = Range;
    opts.maxevals=100;
    opts.maxits=2000;
    opts.maxdeep=2000;
    opts.testflag=0;
    opts.showits=0;
    opts.globalmin =0;
    Problem.f = 'findtheta';
    [FTT1,Xtheta1] = Direct(Problem,bounds,opts);
    if FTT1<FTT
        Xtheta=Xtheta1;
        FTT=FTT1;
    end
end
theta0=Xtheta;
  % Given theta
  theta = theta0(:);   %%%%%%%%%%%%%%%%%%%%%
  [f  fit] = objfunc(theta, par);
  perf = struct('perf',[theta; f; 1], 'nv',1);
%   if  isinf(f)
%     error('Bad point.  Try increasing theta0')
%   end

% Return values
dmodel = struct('regr',regr, 'corr',corr, 'theta',theta.', ...
  'beta',fit.beta, 'gamma',fit.gamma, 'sigma2',sY.^2.*fit.sigma2, ...
  'S',S, 'Ssc',[mS; sS], 'Ysc',[mY; sY], ...
  'C',fit.C, 'Ft',fit.Ft, 'G',fit.G);
end



