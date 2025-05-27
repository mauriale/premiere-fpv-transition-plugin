/**
 * ExtendScript functions for applying FPV effects in Premiere Pro
 */

// Apply FPV effect to a clip
function applyFPVEffect(clip, tiltAngle, panAngle, rollAngle) {
    if (!clip || !clip.projectItem) {
        alert("Please select a clip");
        return false;
    }
    
    try {
        // Add Basic 3D effect
        var basic3D = clip.addVideoEffect("ADBE Basic 3D");
        
        // Set rotation parameters
        if (basic3D) {
            // Swivel = X rotation (tilt)
            basic3D.property("ADBE Basic3D-0001").setValue(tiltAngle);
            
            // Tilt = Y rotation (pan)
            basic3D.property("ADBE Basic3D-0002").setValue(panAngle);
            
            // Distance to Image = Z position
            basic3D.property("ADBE Basic3D-0003").setValue(0);
            
            // Specular Highlight
            basic3D.property("ADBE Basic3D-0004").setValue(0);
            
            return true;
        }
    } catch (e) {
        alert("Error applying FPV effect: " + e.toString());
        return false;
    }
}

// Create keyframes for smooth transition
function createTransitionKeyframes(clip, startRotation, endRotation, duration) {
    try {
        var basic3D = null;
        
        // Find Basic 3D effect
        for (var i = 0; i < clip.videoEffects.numItems; i++) {
            if (clip.videoEffects[i].displayName === "Basic 3D") {
                basic3D = clip.videoEffects[i];
                break;
            }
        }
        
        if (!basic3D) {
            alert("Basic 3D effect not found");
            return false;
        }
        
        // Get clip start time
        var startTime = clip.start.seconds;
        
        // Add keyframes for each rotation axis
        var properties = [
            "ADBE Basic3D-0001", // Swivel
            "ADBE Basic3D-0002"  // Tilt
        ];
        
        for (var i = 0; i < properties.length; i++) {
            var prop = basic3D.property(properties[i]);
            if (prop.canSetTimeVarying()) {
                prop.setTimeVarying(true);
                
                // Start keyframe
                prop.addKey(startTime);
                prop.setValueAtKey(startTime, startRotation[i]);
                
                // End keyframe
                prop.addKey(startTime + duration);
                prop.setValueAtKey(startTime + duration, endRotation[i]);
                
                // Set interpolation to bezier for smooth motion
                prop.setInterpolationTypeAtKey(startTime, 5); // Bezier
                prop.setInterpolationTypeAtKey(startTime + duration, 5);
            }
        }
        
        return true;
    } catch (e) {
        alert("Error creating keyframes: " + e.toString());
        return false;
    }
}

// Get current rotation values from clip
function getCurrentRotation(clip) {
    var rotation = [0, 0, 0];
    
    try {
        // Find Basic 3D effect
        for (var i = 0; i < clip.videoEffects.numItems; i++) {
            if (clip.videoEffects[i].displayName === "Basic 3D") {
                var basic3D = clip.videoEffects[i];
                rotation[0] = basic3D.property("ADBE Basic3D-0001").getValue();
                rotation[1] = basic3D.property("ADBE Basic3D-0002").getValue();
                break;
            }
        }
    } catch (e) {
        // Return default rotation if error
    }
    
    return rotation;
}

// Export functions for CEP panel
if (typeof exports !== 'undefined') {
    exports.applyFPVEffect = applyFPVEffect;
    exports.createTransitionKeyframes = createTransitionKeyframes;
    exports.getCurrentRotation = getCurrentRotation;
}