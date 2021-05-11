clear;clc;
%% Tutorials for learning
% rtbdemo

%% Initial setting
l0 = 0;
l1 = 0;
l2 = 25; % 第一根连杆长度
l3 = 45; l3_v = -10;
l4 = 40; % 3,4
l5 = 5;

L0 = Link('d', 0, 'a', l0, 'alpha', 0, 'modified', 'offset', pi/2 + pi);
L1 = Link('d', 0, 'a', l1, 'alpha', pi/2, 'modified');
L2 = Link('d', 0, 'a', l2, 'alpha', 0, 'modified'); % 1,2
L3 = Link('d', l3_v, 'a', l3, 'alpha', pi/2, 'modified'); % 2,3
L4 = Link('d', l4, 'a', 0, 'alpha', pi/6, 'modified'); % 3,4
L5 = Link('d', l5, 'a', 0, 'alpha', 0, 'modified'); % 4,5 waiting for moving joint

bot = SerialLink([L0 L1 L2 L3 L4 L5], 'name', 'robot');
% initial angle/distance setting
theta = -atan2(l3_v, l3);
q0 = 0;
q1 = 2*pi/3;
q2 = - q1;
q3 = pi/6;
q4 = 0;
q5 = 0;
figure(1);
bot.plot([q0 q1 q2 q3 q4 q5]);
hold on;

%%
% %% step1 : cartesain2T
% resolution = 10;
% y = path(7:end,2) ./ resolution;
% z = path(7:end,1) ./ resolution;
% num = size(y,1);
% T_many = zeros(num, 4, 4);
% for i = 1:num
%     T_many(i,:,:) = [0 -1 0 z(i);
%         1 0 0 y(i);
%         0 0 1 0;
%         0 0 0 1];
% 
% end
% % t1 = fkine(bot,[q0 q1 q2 q3 q4 q5]);
% mask = [1,1,1,1,1,1];
% q_default = zeros(6,num);
% for j = 1:20
%     q_default(:,j) = [0 2.13 -3.04 0.58 1.89 0];
% end
% 
% t_r = zeros(4,4,num);
% q_v = zeros(6,num);
% t = zeros(4,4,num);
% for i = 1:num
%     t_r(:,:,i) = [0 -1 0 0;
%             1 0 0 y(i);
%             0 0 1 z(i);
%             0 0 0 1];
%     q_v(:,i) = ikine(bot,t_r(:,:,i),q_default(i),mask);
%     
% %     if q_v(2,i) < 0
% %         i = i - 1;
% %         continue;
% %     end
%     t(:,:,i) = fkine(bot,q_v(:,i));
%     fprintf('i am caculating number %d path\n',(i));
% end

% %% walls
% figure();
% thick = 0.1;
% x_w = 2;
% z1_h = 1.5; % 2;
% z1_l = 0;
% z2_h = 4;
% z2_l = 2.5; % 2;
% vertices1=[-x_w 2-thick z1_l; -x_w 2+thick z1_l; -x_w 2+thick z1_h; -x_w 2-thick z1_h; x_w 2-thick z1_l; x_w 2+thick z1_l; x_w 2+thick z1_h; x_w 2-thick z1_h;];
% vertices2=[-x_w 3-thick z2_l; -x_w 3+thick z2_l; -x_w 3+thick z2_h; -x_w 3-thick z2_h; x_w 3-thick z2_l; x_w 3+thick z2_l; x_w 3+thick z2_h; x_w 3-thick z2_h;];
% faces=[1 2 6 5;2 3 7 6;3 4 8 7;4 1 5 8;1 2 3 4;5 6 7 8 ];
% for i = 1 : 6
%     h = patch(vertices1(faces(i,:),1),vertices1(faces(i,:),2),vertices1(faces(i,:),3),'g');
%     set(h,'facealpha',0.2);
% end
% for i = 1 : 8
%     text(vertices1(i,1),vertices1(i,2),vertices1(i,3),num2str(i));
% end
% hold on;
% for i = 1 : 6
%     h = patch(vertices2(faces(i,:),1),vertices2(faces(i,:),2),vertices2(faces(i,:),3),'g');
%     set(h,'facealpha',0.2);
% end
% for i = 1 : 8
%     text(vertices2(i,1),vertices2(i,2),vertices2(i,3),num2str(i));
% end
% hold on;
% % view(3);
% %% plot animation
% mid_point = 5;
% q_all = zeros(6, (num-1) * mid_point);
% for i = 1:num-1
%     fprintf('i am plotting number %d animation\n',(i));
%     T = ctraj(t(:,:,i), t(:,:,i+1), mid_point); % compute a Cartesian path
%     q = bot.ikine(T);
% %     if(i >= 7)
% %         bot.plot(q);
% %     end
%     bot.plot(q)
%     q_all(:,i*mid_point:i*mid_point+mid_point-1) = q';
% end
% 
% % pause;
% figure();
% for i = 1:6
%     plot(q_all(i,:));
%     title('Angle transform');
%     hold on;
% end
% %% plot angle curves
% step = 50;
% %轨迹规划方法
% q = zeros(step*num,6);
% qd = zeros(step*num,6);
% qdd = zeros(step*num,6);
% for i = 1:num-1
%     init_ang = q_v(:,i);
%     targ_ang = q_v(:,i+1);
%     [b,bd,bdd] = jtraj(init_ang,targ_ang,step);%直接得到角度、角速度、角加速度的的序列
%     q((i-1)*step+1:i*step,:) = b;
%     qd((i-1)*step+1:i*step,:) = bd;
%     qdd((i-1)*step+1:i*step,:) = bdd;
% end
% %动画显示
% figure()
% 
% %显示位置、速度、加速度变化曲线
% subplot(3, 2, 2);
% for i = 2:5
%     plot(q(:,i));
%     hold on;
% end
% title('位置');
% grid on;
% 
% subplot(3, 2, 4);
% for i = 2:5
%     plot(qd(:,i));
%     hold on;
% end
% title('速度');
% grid on;
% 
% subplot(3, 2, 6);
% for i = 2:5
%     plot(qdd(:,i));
%     hold on;
% end
% title('加速度');
% grid on;
% 
% subplot(3,2,[1,3]); %subplot 对画面分区，【1.3】占用1 3的位置，3.2三行两列
% bot.plot(q);






    

    


