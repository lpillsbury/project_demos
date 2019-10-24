%Leah Pillsbury
%This function takes in a training data matrix Xtrain, training
%label vector ytrain and uses them to compute the average cat
%and dog vectors. It also takes in a test data matrix Xtest and 
%produces a vector of label guesses yguess. Each guess is found
%by searching through Xtrain to find the closest row, and then 
%outputting its label.
function yguess = nearest_neighbor(Xtrain,ytrain,Xtest)
    [m_te,~] = size(Xtest);
    %[m_tr,~] = size(Xtrain);
    yguess = zeros(m_te,1); %preallocate yguess
    % step through each row of Xtest and take the norm of that row with all
    % the rows of Xtrain. then find index of the minimum and make yguess at
    % that row equal the label of the minimum
    for i=1:m_te
        diff = Xtrain-Xtest(i,:);
        neighbor_mat = sqrt(sum(diff.^2,2));
        idx = find(neighbor_mat==min(neighbor_mat));
        % what happens if there are multiple minima?
        yguess(i) = ytrain(idx);
    end
    % running this on cats and dogs dataset where 10% is test set, accuracy
    % is 82.5%. if 30% of data is test set, accuracy is 78.33
end