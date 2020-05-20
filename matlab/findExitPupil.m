function [pupil,surfaces] = findExitPupil(surfaces,sourceAperture,display)
%% find an exit pupil that is an optical conjugate of the first mirror
% inputs: surfaces is a cell array of optical surfaces, sourceAperture is a
% structure describing the ray origins
% outputs: pupil is the surface, index is where it goes in the surface 
% list, h is a plot handle. 

if nargin < 3
    display = false;
end

%% setup 
src = sourceColumn(sourceAperture,0,1); % single ray at center of aperture
options.segments = false;
options.aperture = false;
%% find an image by tracing from the source aperture. 

scale = src.aperture/100;

%% find a pupil
% look for the optical conjugate of the first surface before the last image
% plane

% first, trace the source chief ray to the first surface

r = raytrace(src,surfaces{1},options); %t1{2}; % first surface intersection, instead of ;


if display
    if isnumeric(display)
        figure(display); clf;
    elseif ~ishandle(gcf)
        figure();
    end
    
    subplot(2,5,[1,6]); 
    plotRays({src,r},'b');
    plotApertures(surfaces,true);
    axis equal;
end

% add a differential ray that intersects the curved pupil surface, 1urad
% offset in angle, and then trace that until the end 

rp.N = 2;
rp.position = repmat(r.position(r.chief,:),2,1);
rp.direction(1,:) = r.direction(r.chief,:);
rp.direction(2,:) = (rotationMatrix(r.local(1,:),-1e-4)*r.direction(r.chief,:)')';
rp.valid = [true;true];
rp.opl = [0;0];

% now trace that to the end 
t2 = raytrace(rp,surfaces(2:end),options);
r2 = t2{end};

if display
    hold on;
    plotRays(t2,'r');
end

%pimg is where the chief ray strikes the focus plane
pimg = r2.position(1,:); 
% now find where those rays intersect to define the radius of the pupil
% surface
[ppupil,d] = lineIntersection(r2.position,r2.direction);
disp(sprintf('Pupil after surface (%s) at %d %d %d',r2.surface.name,ppupil));

if display
    scatter3(ppupil(1),ppupil(2),ppupil(3),'r');  
    text(ppupil(1),ppupil(2),ppupil(3),'Pupil relay','color','r','HorizontalAlignment','center'); 
    plot3([ppupil(1), ppupil(1); r2.position(1,1), r2.position(2,1)], ...
        [ppupil(2), ppupil(2); r2.position(1,2), r2.position(2,2)], ...
        [ppupil(3), ppupil(3); r2.position(1,3), r2.position(2,3)],'g');
    hold off;
end
%% new pupil surface

dV = ppupil - pimg;
direction = r2.direction(1,:);
ROC = sqrt(dot(dV,dV));

image = surfaces{end};

pupil = struct;
pupil.name = 'Pupil relay';
pupil.position = ppupil; % vertex tangent
pupil.opdOffset = dot(dV,direction); %negative means virtual
pupil.cuy = sign(pupil.opdOffset) / ROC; %sqrt(sum((dV).^2)); % positive = concave
pupil.direction = sign(pupil.opdOffset) * direction; 
pupil.local = surfaceLocal(pupil);
pupil.center=[0,0,0];
pupil.display = 'nm';

if pupil.opdOffset < 0
    surfaces{end+1} = pupil; 
    % virtual pupil relay, so do a negative trace after computing the image
else
    surfaces{end} = pupil; 
    % real pupil relay, so stop there
end
%%  plot summary
if display
    source = sourceColumn(sourceAperture,3,1);
    source.units = 'mm';
    source.display = 'nm';
    options.negative = true;
    trace = raytrace(source,surfaces,options);
    
    subplot(2,5,3); [p1,mask] = displayOPL(trace{end-1});
    
    subplot(2,5,4);	p2 = displayOPL(trace{end});
    
    subplot(2,5,5); 
    dp = p1-p2;
    dp(mask) = dp(mask) - dp(trace{end}.chief);
    img =  imagesc(1e6*dp); title(sprintf('Difference: %5.5g nm',1e6*std(dp(mask(:)))));
    set(img,'AlphaData',mask); axis image
 
    subplot(2,5,8); plotSpot(trace{end-2});  title(trace{end-2}.surface.name);
    
    subplot(2,5,9); plotSpot(trace{end-1});  title(trace{end-1}.surface.name);
    
    subplot(2,5,10); plotSpot(trace{end});  title(trace{end}.surface.name);
    
    subplot(2,5,[2 7]); plotRays(trace,'b');plotSurfaces(trace);axis image;
    
    
end
end