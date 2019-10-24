//C++ version of collision program
// Copyright Leah Pillsbury 2018 leahp@bu.edu

#include <iostream>
#include <vector>
#include <math.h>
#include <string>
#include <sstream>
#include <algorithm>

using std::cin;
using std::string;
using std::cout;
using std::vector;
using std::stod;
using std::ostringstream;


//function declarations
vector <double> get_timestamp(int argc, char *argv[]);
void process_input();
void print_output(double time);
double will_collide(int ind1, int ind2);
double calc_next_collision();
void move(double time);
void collision();

class Disk{
      //vector <double> pos;   //position of disk
      //vector <double> vel;
    public:
        double x, y, vx, vy;
        string ID;
};

//global variables
vector <Disk> disk_list;
vector <int> which_hit(2,-1);

vector <double> get_timestamp(int argc, char* argv[]){
    //get in timestamp from command line
    vector <double> timestamp;
    double timearg;
    std::string::size_type idx;
    int index=0;
    for (int i=1; i<argc; i++){
        try{
            timearg=stod(argv[i], &idx);

        }
        catch(...){
            exit(2);
        }
        if(timearg<0){
            continue;
        }
        else{
            timestamp.push_back(timearg);
            //cout<<timestamp[index];
            index=index+1;
        }
    }
    sort(timestamp.begin(),timestamp.end());
    if(timestamp.empty()){
        exit(2);
    }
    //for (int i=0; i<index; i++){
        //cout<<timestamp[i]<<'\n';
    //}
    return timestamp;
}

void process_input(){
     //string s;
    string line;
    Disk thisentry;

    while (true) {
        getline(cin,line);
        if (cin.eof()) break;
        std::stringstream ss(line);

        string name;
        double x,y,vx,vy;

        ss >> thisentry.ID;
        ss >> thisentry.x;
        ss >> thisentry.y;
        ss >> thisentry.vx >>thisentry.vy;

        if (ss.fail()) {
            //cout << "fail\n";
            exit(1);
        }
        string rest;
        ss >> rest;
        if (!ss.fail()) {
            //cout << "fail on end\n";
            exit(1);
        }
        disk_list.push_back(thisentry);
        //cout << name << x << " " << y << " " << vx << " "<< vy << "\n";
    }
}

void print_output(double time){
    cout<<time<<'\n';
    int length=disk_list.size();
    //string str_to_print;
    //std::stringstream os(str_to_print);

    for (int i=0; i<length; i++){
        //str_to_print=str(disk_list[i].ID)+" "+str(disk_list[i].x)+" "+str(disk_list[i].y)+" "+str(disk_list[i].vx)+" "+str(disk_list[i].vy);
        cout<<disk_list[i].ID<<" "<<disk_list[i].x<<" "<<disk_list[i].y<<" "<<disk_list[i].vx<<" "<<disk_list[i].vy<<'\n';
    }
}

double will_collide(int ind1, int ind2){
    //this function returns dot product of difference between any two balls and says whether they are going towards each other"
    //they could go towards each other but never hit if they are going towards each other farther away from their radii"
    double x_diff, y_diff, vx_diff, vy_diff, wc;
    x_diff=disk_list[ind1].x-disk_list[ind2].x;
    y_diff=disk_list[ind1].y-disk_list[ind2].y;
    vx_diff=disk_list[ind1].vx-disk_list[ind2].vx;
    vy_diff=disk_list[ind1].vy-disk_list[ind2].vy;
    wc=x_diff*vx_diff+y_diff*vy_diff;
    return wc;
}

double calc_next_collision(){
   //calculates when the next collision will be and returns that time
    double x_diff, y_diff, vx_diff, vy_diff, possible_time=-1;
    for(int z=0; z<disk_list.size()-1; z++){
        int counter=0;
        for(int i=0; i<disk_list.size(); i++){
            for(int j=1; j<disk_list.size(); j++){
                if(i==j){
                    continue;
                }
                else{
                    double a, b, c, x, wc;
                    x_diff=disk_list[i].x-disk_list[j].x;
                    y_diff=disk_list[i].y-disk_list[j].y;
                    vx_diff=disk_list[i].vx-disk_list[j].vx;
                    vy_diff=disk_list[i].vy-disk_list[j].vy;
                    c=x_diff*x_diff+y_diff*y_diff-100;
                    b=2*(x_diff*vx_diff+y_diff*vy_diff);
                    a=vx_diff*vx_diff+vy_diff*vy_diff;
                    //cout<<"a "<<a<<"b "<<b<<"c "<<c<<'\n';
                    x=pow(b,2)-4*a*c;
                    //cout<<"x "<<x<<'\n';
                    wc=will_collide(i,j);
                    if (x>=0 && wc<0){
                        double t1=(-b-sqrt(pow(b,2)-4*a*c))/(2*a);
                        if (t1>0 ||abs(t1)<1e-8){
                            if (abs(t1)<1e-8){
                                t1=0;
                            }
                            if (counter==0 || t1<possible_time){
                                possible_time=t1;
                                which_hit[0]=i;
                                which_hit[1]=j;
                            }
                        }
                    }

                }
                counter=counter+1;
            }
        }

    }
    return possible_time;
}

void move(double time){
    for (int i=0; i<disk_list.size();i++){
        disk_list[i].x=disk_list[i].x+disk_list[i].vx*time;
        disk_list[i].y=disk_list[i].y+disk_list[i].vy*time;
    }
}

void collision(){
    //computes transfer of momentum at collision at exactly the time of hit. no instantaneous position change"
    double x_diff, y_diff, vx_diff, vy_diff, numerator, denominator, q;
    double new_vx1, new_vy1, new_vx2, new_vy2;
    int i=which_hit[0], j=which_hit[1];

    //calculate updated velocity for one of the disks
    x_diff=disk_list[i].x-disk_list[j].x;
    y_diff=disk_list[i].y-disk_list[j].y;
    vx_diff=disk_list[i].vx-disk_list[j].vx;
    vy_diff=disk_list[i].vy-disk_list[j].vy;
    numerator=vx_diff*x_diff+vy_diff*y_diff;
    denominator=x_diff*x_diff+y_diff*y_diff;
    q=numerator/denominator;
    new_vx1=disk_list[i].vx-q*x_diff;
    new_vy1=disk_list[i].vy-q*y_diff;

    //calculate updated velocity for other disk
    x_diff=disk_list[j].x-disk_list[i].x;
    y_diff=disk_list[j].y-disk_list[i].y;
    vx_diff=disk_list[j].vx-disk_list[i].vx;
    vy_diff=disk_list[j].vy-disk_list[i].vy;
    numerator=vx_diff*x_diff+vy_diff*y_diff;
    denominator=x_diff*x_diff+y_diff*y_diff;
    q=numerator/denominator;
    new_vx2=disk_list[j].vx-q*x_diff;
    new_vy2=disk_list[j].vy-q*y_diff;

    disk_list[i].vx=new_vx1;
    disk_list[i].vy=new_vy1;
    disk_list[j].vx=new_vx2;
    disk_list[j].vy=new_vy2;
}


int main (int argc, char* argv[]){
    vector <double> timestamp=get_timestamp(argc, argv);
    process_input();
    double master_time=0, collision_time;
    if(disk_list.size()==1){
    //don't worry about collisions if there is only one disk"
        for (int i=0; i<timestamp.size(); i++){
            move(timestamp[i]-master_time);
            print_output(timestamp[i]);
            master_time=timestamp[i];
        }

    }
    else{
        for(int i=0; i<timestamp.size(); i++){
            collision_time=calc_next_collision();
            while((collision_time+master_time)<=timestamp[i] && collision_time>=0){
                master_time=master_time+collision_time;
                while(collision_time==0){
                    collision();
                    collision_time=calc_next_collision();
                    //cout<<"collision time is "<<collision_time<<'\n';
                    //cout<<"which hit "<<which_hit[0]<<which_hit[1]<<'\n';
                }
                if (collision_time>0){
                    move(collision_time);
                    collision();
                    collision_time=calc_next_collision();
                }
            }
            double time_forward=timestamp[i]-master_time;
            move(time_forward);
            master_time=timestamp[i];
            print_output(timestamp[i]);
        }
    }
    return 0;
}

