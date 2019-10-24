% Leah Pillsbury
% this function uses matlab's built in PCA function to find top 10
% eigenvectors and display their images (eigenfaces) as explained in
% problem 7.5
function run_pca(Xtrain)
    coeff = pca(Xtrain);
    eig = (coeff(:,1:10))'; %matrix of top 10 eigenvectors where each row is a vector
    for i=1:10
        show_image(eig,i)
    end
    
end