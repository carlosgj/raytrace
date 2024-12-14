import logging
from raytrace import Surface
from Source import PointSource

logging.basicConfig(level=logging.DEBUG)

#Example 001: point source through a tilted rectangular prism

#[start, finish] = importVV('example_001_VV.txt');

#setup
#BS front surface
s1=Surface(name='s1')
s1.setPosition([0,0,70])
s1.setDirection([0,-1,1])
s1.setType(2) #0=reference, 1=reflect, 2=refract
s1.setIndex(1.518522387620793)


# BS back surface
s2=Surface(name='s2')
s2.setPosition([0, 0, 80])
s2.setDirection(s1.direction)
s2.setType(2)
s2.setIndex(1)


# Stop
s3=Surface(name='s3')
s3.setPosition([0,0,120])
s3.setDirection([0,0,1])
s3.setType(0)


# trace 1e3 times in 2 seconds
#source = sourcePoint([0,0,0],[0,0,1],[1,0,0],.1,10);
source = PointSource([0,0,0], [0,0,1], [1,0,0], 0.1, 10)
rays = source.makeRays()
surfaces = {s1, s2, s3};

'''
tic
trace = raytrace(source, surfaces);
toc
%%
clf;
plotSurfaces(trace);
axis equal; view(normr([1,0,1]));camroll(-90);
hold on;plotRays(trace,'b');hold off;

%% compare
% disp('accuracy')
% std(rays.position - finish.position,1)
% std(rays.direction - finish.direction,1)
'''
