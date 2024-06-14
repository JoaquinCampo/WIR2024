import React, { useEffect } from "react";
import ScrollMagic from "scrollmagic";
import { gsap } from "gsap";
import { ScrollMagicPluginGsap } from "scrollmagic-plugin-gsap";
import "scrollmagic/scrollmagic/uncompressed/plugins/debug.addIndicators";

import "../styles/App.css"

// Enable ScrollMagic to use GSap for animations
ScrollMagicPluginGsap(ScrollMagic, gsap);
const Scroll = () => {
  useEffect(() => {
    // Initialize ScrollMagic controller
    const controller = new ScrollMagic.Controller();

    // Create a tween (animation)
    const tween = gsap.to(".animate", {
      duration: 0.5,
      opacity: 1,
      y: -50,
      ease: "power1.inOut"
    });

    // Create a ScrollMagic scene
    new ScrollMagic.Scene({
      triggerElement: ".trigger",
      triggerHook: 0.5,
      reverse: false,
    })
      .setTween(tween)
      .addIndicators() // Add indicators (requires plugin)
      .addTo(controller);

    // Cleanup on unmount
    return () => {
      controller.destroy(true);
    };
  }, []);

  return (
    <div>
      <div className="spacer" style={{ height: "100vh" }}>
        Scroll down to see the animation
      </div>
      <div className="trigger" style={{ height: "100vh", backgroundColor: "#f0f0f0" }}>
        <div className="animate" style={{ opacity: 0 }}>
          I'm an animated element
        </div>
      </div>
    </div>
  );
};

export default Scroll;

