clear;clc;
%% Initial setting
l0 = 0;
l1 = 0;
l2 = 16.3; % The length of first rod
l3 = 30; % 20
l4 = 30; % 
l5 = 5;

L0 = Link('d', 0, 'a', l0, 'alpha', 0, 'modified', 'offset', pi/2 + pi);
L1 = Link('d', 0, 'a', l1, 'alpha', pi/2, 'modified');
L2 = Link('d', 0, 'a', l2, 'alpha', 0, 'modified'); % 1,2
L3 = Link('d', 0, 'a', l3, 'alpha', pi/2, 'modified'); % 2,3
L4 = Link('d', l4, 'a', 0, 'alpha', pi/6, 'modified'); % 3,4
L5 = Link('a', 0, 'alpha', 0, 'prismatic', 'modified', 'offset', 0); % 4,5 waiting for moving joint

L0.qlim = [-pi/2 pi/2];
L1.qlim = [-pi/2 pi/2];
L2.qlim = [-pi/2 pi/2];
L3.qlim = [-pi/2 pi/2];
L4.qlim = [-pi/2 pi/2];
L5.qlim = [0 5];
bot = SerialLink([L0 L1 L2 L3 L4 L5], 'name', 'robot');
% initial angle/distance setting
figure(1);
% teach(bot); 
theta = [0  pi+pi/8 -pi+pi/6 0 0 0];
bot.plot(theta);
fprintf('Completed init! Waiting for continuing!\n');
pause;
hold on;

bot.display();
%% Draw reachable space
N=30000;    %随机次数

%关节角度限制
limitmax_1 = 0.0;
limitmin_1 = 90.0;
limitmax_2 = -90.0;
limitmin_2 = 90.0;
limitmax_3 = -90.0;
limitmin_3 = 90.0;
limitmax_4 = -90;
limitmin_4 = 90.0;
limitmax_5 = -90.0;
limitmin_5 = 90.0;
limitmax_6 = 0;
limitmin_6 = 5;

theta1=(limitmin_1+(limitmax_1-limitmin_1)*rand(N,1))*pi/180; %关节1限制
theta2=(limitmin_2+(limitmax_2-limitmin_2)*rand(N,1))*pi/180; %关节2限制
theta3=(limitmin_3+(limitmax_3-limitmin_3)*rand(N,1))*pi/180; %关节3限制
theta4=(limitmin_4+(limitmax_4-limitmin_4)*rand(N,1))*pi/180; %关节4限制
theta5=(limitmin_4+(limitmax_4-limitmin_4)*rand(N,1))*pi/180; %关节5限制
theta6=(limitmin_4+(limitmax_4-limitmin_4)*rand(N,1)); %关节6限制

qq=[theta1,theta2,theta3,theta4,theta5,theta6];

Mricx=bot.fkine(qq);
X=zeros(N,1);
Y=zeros(N,1);
Z=zeros(N,1);
for n=1:1:N
    X(n)=Mricx(n).t(1);
    Y(n)=Mricx(n).t(2);
    Z(n)=Mricx(n).t(3);

end
plot3(X,Y,Z,'b.','MarkerSize',0.5);%画出落点
hold on;
fprintf('Complete reachable space potting! Waiting for continuing!\n');
pause;
%% Cartesain2T
T1 = bot.fkine([0  pi+pi/8 -pi+pi/6 0 0 0]);
% T2 = bot.fkine([0 5*pi/6 -pi+pi/6 pi/2 0 0]);
n = 10;
for i = 1:n
    theta = [0 pi+pi/8-i*7*pi/24/n -pi+pi/6 i*pi/2/n 0 0];
    T2 = bot.fkine(theta);
    q1=bot.ikine(T1);%根据起始点位姿，得到起始点关节角
    q2=bot.ikine(T2);%根据终止点位姿，得到终止点关节角
    [q ,qd, qdd]=jtraj(q1,q2,300/n); %五次多项式轨迹，得到关节角度，角速度，角加速度，50为采样点个数
    grid on
    % T=bot.fkine(q);%根据插值，得到末端执行器位姿
    % plot3(squeeze(T(1,4,:)),squeeze(T(2,4,:)),squeeze(T(3,4,:)));%输出末端轨迹
    hold on
    if(i ~= 5)
        subplot(3,2,[1,3]);
        bot.plot(q); 
        
        subplot(3,2,2);
        i=1:6;
        plot(q(:,i));
        title('位置');
        grid on;
        subplot(3,2,4);
        i=1:6;
        plot(qd(:,i));
        title('速度');
        grid on;
        subplot(3,2,6);
        i=1:6;
        plot(qdd(:,i));
        title('加速度');
        grid on;

        Tc=ctraj(T1,T2,30);
        Tjtraj=transl(Tc);
        subplot(3,2,5);
        plot2(Tjtraj,'r');
        title('轨迹');
        grid on;
    end
    T1 = T2;
end
fprintf('THE END!!!');

