function lab1()
    X = [-0.23,-1.03,-4.11,-0.65,-2.58,-0.79,-1.53,-0.18,-2.79,-1.97,-2.21,-1.59,-0.22,-3.18,-1.18,-1.42,-1.29,-2.22,-0.82,-1.87,-2.30,-0.94,-0.74,-2.45,-1.40,-2.09,-0.68,0.02,-1.80,-2.25,-1.19,-2.17,-1.89,-1.14,-1.50,-1.76,-0.69,-2.21,-1.65,-1.51,-2.11,-2.24,-0.72,0.94,-0.67,-2.44,-2.27,-1.33,-3.03,-0.42,-2.86,-2.00,-1.37,-1.90,-2.80,-0.89,-2.04,-1.66,-0.14,-2.79,-0.21,-1.29,-2.81,-0.29,-1.55,-0.45,-1.16,-3.96,-3.77,-3.36,-1.81,0.13,-2.61,-3.69,-3.00,-2.61,-0.74,-0.41,-0.78,-1.49,-1.89,-1.24,-0.00,-2.72,-1.69,-1.25,-1.59,0.20,-1.08,-2.42,-3.14,-2.54,-2.09,-2.51,-2.65,-2.42,-1.30,-0.65,1.40,-2.33,-1.97,-0.54,-1.13,-2.04,0.77,-1.03,-1.55,-1.47,-0.09,-2.11,-2.08,-1.79,-1.36,-1.92,-3.04,-1.08,-1.67,-2.11,-1.99,-1.64];
    X = sort(X);
    
    Mmax = max(X);
    Mmin = min(X);
    
    fprintf('Mmin = %s\n', num2str(Mmin));
    fprintf('Mmax = %s\n', num2str(Mmax));
    
    R = Mmax - Mmin;
    fprintf('R = %s\n', num2str(R));
    
    MU = getMU(X);
    fprintf('MU = %s\n', num2str(MU));
    
    Ssqr = getSsqr(X);
    fprintf('S^2 = %s\n', num2str(Ssqr));
    
    m = getNumberOfIntervals(X);
    fprintf('m = %s\n', num2str(m))
    
    createGroup(X);
    hold on;
    distributionDensity(X, MU, Ssqr, m);

    figure;
    empiricF(X);
    hold on;
    distribution(X, MU, Ssqr, m);
end

function mu = getMU(X)
    n = length(X);
    mu = sum(X)/n;
end

function Ssqr = getSsqr(X)
    n = length(X);
    MX = getMU(X);
    Ssqr = sum((X - MX).^2) / (n-1);
end

function m = getNumberOfIntervals(X)
    m = floor(log2(length(X)) + 2);
end

function createGroup(X)
    n = length(X);
    m = getNumberOfIntervals(X);
    
    intervals = zeros(1, m+1);
    numCount = zeros(1, m+1);
    Delta = (max(X) - min(X)) / m;
    
    for i = 0: m
        intervals(i+1) = X(1) + Delta * i;
    end
    
    j = 1;
    count = 0;
    for i = 1:n
        if (X(i) >= intervals(j+1)) 
            j = j + 1; 
        end
        numCount(j) = numCount(j) + 1;
        count = count + 1;
    end

	graphBuf = numCount(1:m+1);
    for i = 1:m+1
        graphBuf(i) = numCount(i) / (n*Delta); 
    end
    
    stairs(intervals, graphBuf),grid;
end

function distributionDensity(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    Sigma = sqrt(DX);
    
    Xn = (MX - R): delta/50 :(MX + R);
    Y = normpdf(Xn, MX, Sigma);
    plot(Xn, Y), grid;
end

function distribution(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    
    Xn = (MX - R): delta :(MX + R);
    Y = 1/2 * (1 + erf((Xn - MX) / sqrt(2*DX))); 
    plot(Xn, Y, 'r'), grid;
end

function empiricF(X)  
    [yy, xx] = ecdf(X);
    
    stairs(xx, yy), grid;
end