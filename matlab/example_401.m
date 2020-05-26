% Example 401: test zernike perturbation

%% setup
% mirror -- note the mirror has no curvature, just a big focus aberration
s1=struct();
s1.position = [0,0,10];
s1.direction=[0,0,-1];
s1.zernike=[0 0 0 1 .3 ]; % focus and astigmatism. Units are mm, not waves.
s1.local=[1 0 0; 0 1 0];
s1.aperture.type  = 'annulus';
s1.aperture.radius = [3 10];
s1.type = 'reflect';
% Stop
s3=struct();
s3.position = [0,0,-1];
s3.direction=[0,0,1];

%% raytrace
source = sourceColumn([0,0,0],[0,0,1],[1,0,0],10,5);
surfaces = {s1, s3};

tic
trace = raytrace(source, surfaces);
toc
%% what's that look like?
clf;
subplot(1,3,1);
viewaxes = [0 0 1;0 1 0]';
plotSideView(trace,viewaxes,'b','LineWidth',2);
axis equal; 

subplot(1,3,2)
plotSurfaces(trace);sideview;view([1,0,.5]);
axis equal;
hold on;plotRays(trace,'b');hold off;

subplot(1,3,3)
plotApertures(s1);hold on; plotSpot(trace{2},'b');hold off;
axis equal; grid on;


%% compare
% std(rays.position - finish.position,1)
% std(rays.direction - finish.direction,1)
