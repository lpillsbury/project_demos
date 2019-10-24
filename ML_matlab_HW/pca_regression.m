%Leah Pillsbury
%This function takes in a training data matrix Xtrain, training
%label vector ytrain and uses them to compute the PCA basis. 
%It also takes in a test data matrix Xtest and a dimension k
%and uses the top-k vectors in the PCA basis to reduce the 
%dimension of Xtrain and Xtest. Finally, it uses the reduced data
%as inputs to the linear_regression function to produce 
%a vector of label guesses yguess.
function yguess = pca_regression(Xtrain,ytrain,Xtest,k)
%     [mtr,~] = size(Xtrain);
%     [mte,~] = size(Xtest);
% 
%     mu_Xtr = 1/mtr * (Xtrain'*ones(mtr,1)); %(this is the average xtrain vector it is 4096x1)
%     X_tr_centered = Xtrain-ones(mtr,1)*mu_Xtr';
%     diff=bsxfun(@minus,Xtrain,mu_Xtr');  %this is the same as previous
%     %line
%     cov_Xtr = (diff'* diff)./mtr;
%     [V,D] = eig(cov(diff)); %cov(diff) is same as cov_Xtr
%     V_k = V(:,1:k); 
%     X_tr_reduced = X_tr_centered*V_k;
% 
%     % do the same process again for the test matrix
%     mu_Xte = 1/mte * (Xtest'*ones(mte,1));
%     X_te_centered = Xtest-ones(mte,1)*mu_Xte';
%     diff=bsxfun(@minus,Xtest,mu_Xte');
%     %cov_Xte = (diff'* diff)./mte;
%     % cov(diff) matches cov_Xte and cov(X_te_centered)
%     X_te_reduced = X_te_centered*V_k;

    % yguess=linear_regression(X_tr_reduced, ytrain, X_te_reduced);
    % when k=10, accuracy is 49.5%. same accuracy for different k values.
    % covariance matrix is deffinitely right (checked three ways); maybe missing a transpose
    % somewhere else? tried transposing eigenvectors also didn't help.
    % another problem was using V and mu different for training and test
   
    % alternatively, using PCA function:
    % also, realized that V_k should be from test set
    % mu is also the mu from training, dont take average from test
    [mtr,~] = size(Xtrain);
    [mte,~] = size(Xtest);
    [V,Xtr_r,latent] = pca(Xtrain,'NumComponents',k);
    mu_Xtr = 1/mtr * (Xtrain'*ones(mtr,1)); %(this is the average xtrain vector it is 4096x1)
    X_te_centered = Xtest-ones(mte,1)*mu_Xtr'; %using mu_Xtr because Xtr is bigger so average more representative
    Xte_r = X_te_centered*V;
    yguess=linear_regression(Xtr_r, ytrain, Xte_r);
    % accuracy for k=10 is 87,
    % accuracy for k=20 is 85.5
    % accuracy for k=50 is 91.5
    % accuracy for k=100 is 90
end
