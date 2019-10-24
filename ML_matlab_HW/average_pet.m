%Leah Pillsbury
%This function takes in a data matrix X and a label
%vector y and outputs the average cat image and average dog image.
function [avgcat, avgdog] = average_pet(X,y)
    % all dog images go into one matrix and cat images go into another
    % cats are -1 and dogs are +1
    [m, d] = size(X); % total number of samples and number of pixels per sample
    dog_m = 1; % number of dog samples
    cat_m = 1; % number of cat samples
    Xdog = [];
    Xcat = [];
    for i=1:m
        % for each sample put the cats in the cat matrix and dogs in dog
        % matrix
        if y(i)==1
            Xdog(dog_m,:) = X(i,:);
            dog_m = dog_m + 1; 
        else
            Xcat(cat_m,:) = X(i,:);
            cat_m = cat_m + 1;
        end
    end
    
    avgcat = mean(Xcat); % take the mean of each column 
    avgdog = mean(Xdog);
    % this is more complicated than it needs to be: this func is just find
    % the mean
    % find eigenface for dog and eigenface for cat
    % now what do I do with the V and the Ds?
    %[Vcat,Dcat] = eig(1/m * Xcat'*Xcat);
    %[Vdog,Ddog] = eig(1/m * Xdog'*Xdog);
end
            