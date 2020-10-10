function lab2()
    X=[-0.23,-1.03,-4.11,-0.65,-2.58,-0.79,-1.53,-0.18,-2.79,-1.97,-2.21,-1.59,-0.22,-3.18,-1.18,-1.42,-1.29,-2.22,-0.82,-1.87,-2.30,-0.94,-0.74,-2.45,-1.40,-2.09,-0.68,0.02,-1.80,-2.25,-1.19,-2.17,-1.89,-1.14,-1.50,-1.76,-0.69,-2.21,-1.65,-1.51,-2.11,-2.24,-0.72,0.94,-0.67,-2.44,-2.27,-1.33,-3.03,-0.42,-2.86,-2.00,-1.37,-1.90,-2.80,-0.89,-2.04,-1.66,-0.14,-2.79,-0.21,-1.29,-2.81,-0.29,-1.55,-0.45,-1.16,-3.96,-3.77,-3.36,-1.81,0.13,-2.61,-3.69,-3.00,-2.61,-0.74,-0.41,-0.78,-1.49,-1.89,-1.24,-0.00,-2.72,-1.69,-1.25,-1.59,0.20,-1.08,-2.42,-3.14,-2.54,-2.09,-2.51,-2.65,-2.42,-1.30,-0.65,1.40,-2.33,-1.97,-0.54,-1.13,-2.04,0.77,-1.03,-1.55,-1.47,-0.09,-2.11,-2.08,-1.79,-1.36,-1.92,-3.04,-1.08,-1.67,-2.11,-1.99,-1.64];

    N = 1:length(X);
    
    gamma = 0.9;
    alpha = (1 - gamma)/2;

    mu = expectation(X);
    sSqr = variance(X); 

    fprintf('mu = %.4f\n', mu); 
    fprintf('S^2 = %.4f\n\n', sSqr);

    muArray = expectationArray(X, N);
    varArray = varianceArray(X, N);
 
    figure
    plot([N(1), N(end)], [mu, mu], 'm');
    hold on;
    plot(N, muArray, 'g');
    
    Ml = muArray - sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Ml, 'b');

    fprintf('mu_low = %.4f\n', Ml(end));
    
    Mh = muArray + sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Mh, 'r'), legend('y=mu', 'y=mu_n', 'y=mu-low_n', 'y=mu-high_n');
    grid on;
    hold off;
    
    fprintf('mu_high = %.4f\n', Mh(end));

    figure
    plot([N(1), N(end)], [sSqr, sSqr], 'm');
    hold on;
    plot(N, varArray, 'g');
    
    Sl = varArray.*(N - 1)./chi2inv(1 - alpha, N - 1);
    plot(N, Sl, 'b');
    
    Sh = varArray.*(N - 1)./chi2inv(alpha, N - 1);
    plot(N, Sh, 'r'), legend('z=S^2', 'z=S^2_n', 'z=S^2-low_n', 'z=S^2-high_n');
    grid on;
    hold off;

	
    fprintf('sigma^2_low = %.4f\n', Sl(end));
    fprintf('sigma^2_high = %.4f\n', Sh(end));
end

function mu = expectation(X)
   mu = mean(X);
end

function sSqr = variance(X)
    sSqr = var(X);
end

function muArray = expectationArray(X, N)
    muArray = zeros(1, length(N));
    for i = 1:length(N)
        muArray(i) = expectation(X(1:N(i)));
    end
end

function varArray = varianceArray(X, N)
    varArray = zeros(1, length(N));
    for i = 1:length(N)
        varArray(i) = variance(X(1:N(i)));
    end
end