%Leah Pillsbury
%This function takes in a training data matrix Xtrain, training
%label vector ytrain and uses them to compute ordinary-least-squares
%vector b. It also takes in a test data matrix Xtest and 
%produces a vector of label guesses yguess, corresponding to the sign
%of the linear prediction.
function yguess = linear_regression(Xtrain,ytrain,Xtest)
    [m,~]=size(Xtrain);
    % make a design matrix where first column is ones
    X_design = [ones(m,1), Xtrain];
    mat_inv = pinv(X_design'*X_design);
    b = mat_inv*X_design'*ytrain; 
    % b is a 4097 x 1 double. first entry is y intercept, rest is the
    % weights
    b_0 = b(1);
    b = b(2:length(b));
    yguess = sign(b_0 + Xtest*b);
    % accuracy is 81.2% when test set is 25% of whole training set
end