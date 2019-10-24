%Leah Pillsbury
%This function takes in a training data matrix Xtrain, training
%label vector ytrain and uses them to compute the average cat
%and dog vectors. It also takes in a test data matrix Xtest and 
%produces a vector of label guesses yguess, corresponding to whether
%each row of Xtest is closer to the average cat or average dog.
function yguess = closest_average(Xtrain,ytrain,Xtest)
    m = length(ytrain);
    %find average cat and average dog
    [m, d] = size(Xtrain); % total number of samples and number of pixels per sample
    dog_m = 1; % number of dog samples
    cat_m = 1; % number of cat samples
    Xdog = [];
    Xcat = [];
    for i=1:m
        % for each sample put the cats in the cat matrix and dogs in dog
        % matrix
        if ytrain(i)==1
            Xdog(dog_m,:) = Xtrain(i,:);
            dog_m = dog_m + 1; 
        else
            Xcat(cat_m,:) = Xtrain(i,:);
            cat_m = cat_m + 1;
        end
    end
    
    avgcat = mean(Xcat); % take the mean of each column 
    avgdog = mean(Xdog);
    
    % find L2 distance between a given test and the average cat and the
    % average dog. set yguess= to whichever distance is closer
    [n,d] = size(Xtest);
    yguess = ones(n,1); %preallocate hypothesis matrix for speed
    for i=1:n
        cat_close = norm(Xtest(i,:)-avgcat(1,:));
        dog_close = norm(Xtest(i,:)-avgdog(1,:));
        if cat_close < dog_close
            yguess(i) = -1;
        end
    end
    
    %when running this code on a training and test set, accuracy= 80.1667
end