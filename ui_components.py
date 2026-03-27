import streamlit as st

def render_skeleton_loader():
    """
    Renders a premium dark-mode skeleton loader with a "right shining" effect.
    """
    skeleton_css = """
    <style>
    @keyframes rightShine {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }
    
    @keyframes pulse {
      0% { opacity: 0.5; }
      50% { opacity: 1; }
      100% { opacity: 0.5; }
    }

    .skeleton-container {
        padding: 30px;
        background: rgba(26, 29, 33, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    }

    .skeleton-box {
      display: inline-block;
      height: 20px;
      position: relative;
      overflow: hidden;
      background: linear-gradient(90deg, #21262d 25%, #30363d 50%, #21262d 75%);
      background-size: 200% 100%;
      width: 100%;
      margin-bottom: 14px;
      border-radius: 8px;
    }

    .skeleton-box::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background-image: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.1) 40%,
        rgba(255, 255, 255, 0.3) 50%,
        rgba(255, 255, 255, 0.1) 60%,
        rgba(255, 255, 255, 0) 100%
      );
      animation: rightShine 1.5s infinite linear;
      content: '';
      background-size: 200% 100%;
    }

    .skeleton-header { height: 35px; width: 50%; opacity: 0.8; }
    .skeleton-text { height: 12px; width: 100%; }
    .skeleton-img { height: 160px; width: 100%; opacity: 0.6; }
    
    .loading-text {
        color: #ffffff;
        font-weight: 500;
        font-size: 1.2rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        text-shadow: none;
    }
    
    /* Custom Geometric Loader - Scaled & Left Aligned */
    .loader {
      --color-one: #ffbf48;
      --color-two: #be4a1d;
      --color-three: #ffbf4780;
      --color-four: #bf4a1d80;
      --color-five: #ffbf4740;
      --time-animation: 2s;
      --size: 0.28; /* Further reduced for a sleek fit */
      position: relative;
      border-radius: 50%;
      transform: scale(var(--size));
      transform-origin: center center;
      width: 100px;
      height: 100px;
      flex-shrink: 0;
      margin-left: -35px; /* Adjusted for the smaller scale */
      margin-right: -35px;
      box-shadow:
        0 0 10px 0 var(--color-three),
        0 10px 25px 0 var(--color-four); /* Reduced shadow glow */
      animation: colorize calc(var(--time-animation) * 3) ease-in-out infinite;
    }

    .loader::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100px;
      height: 100px;
      border-radius: 50%;
      border-top: solid 1px var(--color-one);
      border-bottom: solid 1px var(--color-two);
      background: linear-gradient(180deg, var(--color-five), var(--color-four));
      box-shadow:
        inset 0 10px 10px 0 var(--color-three),
        inset 0 -10px 10px 0 var(--color-four);
    }

    .loader .box {
      width: 100px;
      height: 100px;
      background: linear-gradient(
        180deg,
        var(--color-one) 30%,
        var(--color-two) 70%
      );
      mask: url(#clipping);
      -webkit-mask: url(#clipping);
    }

    .loader svg {
      position: absolute;
    }

    .loader svg #clipping {
      filter: contrast(15);
      animation: roundness calc(var(--time-animation) / 2) linear infinite;
    }

    .loader svg #clipping polygon {
      filter: blur(7px);
    }

    .loader svg #clipping polygon:nth-child(1) {
      transform-origin: 75% 25%;
      transform: rotate(90deg);
    }

    .loader svg #clipping polygon:nth-child(2) {
      transform-origin: 50% 50%;
      animation: rotation var(--time-animation) linear infinite reverse;
    }

    .loader svg #clipping polygon:nth-child(3) {
      transform-origin: 50% 60%;
      animation: rotation var(--time-animation) linear infinite;
      animation-delay: calc(var(--time-animation) / -3);
    }

    .loader svg #clipping polygon:nth-child(4) {
      transform-origin: 40% 40%;
      animation: rotation var(--time-animation) linear infinite reverse;
    }

    .loader svg #clipping polygon:nth-child(5) {
      transform-origin: 40% 40%;
      animation: rotation var(--time-animation) linear infinite reverse;
      animation-delay: calc(var(--time-animation) / -2);
    }

    .loader svg #clipping polygon:nth-child(6) {
      transform-origin: 60% 40%;
      animation: rotation var(--time-animation) linear infinite;
    }

    .loader svg #clipping polygon:nth-child(7) {
      transform-origin: 60% 40%;
      animation: rotation var(--time-animation) linear infinite;
      animation-delay: calc(var(--time-animation) / -1.5);
    }

    @keyframes rotation {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    @keyframes roundness {
      0% { filter: contrast(15); }
      20% { filter: contrast(3); }
      40% { filter: contrast(3); }
      60% { filter: contrast(15); }
      100% { filter: contrast(15); }
    }

    @keyframes colorize {
      0% { filter: hue-rotate(0deg); }
      20% { filter: hue-rotate(-30deg); }
      40% { filter: hue-rotate(-60deg); }
      60% { filter: hue-rotate(-90deg); }
      80% { filter: hue-rotate(-45deg); }
      100% { filter: hue-rotate(0deg); }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """
    st.markdown(skeleton_css, unsafe_allow_html=True)

    st.markdown(f'''
    <div class="skeleton-container">
        <div class="loading-text">
            <div class="loader">
              <svg width="100" height="100" viewBox="0 0 100 100">
                <defs>
                  <mask id="clipping">
                    <polygon points="0,0 100,0 100,100 0,100" fill="black"></polygon>
                    <polygon points="25,25 75,25 50,75" fill="white"></polygon>
                    <polygon points="50,25 75,75 25,75" fill="white"></polygon>
                    <polygon points="35,35 65,35 50,65" fill="white"></polygon>
                    <polygon points="35,35 65,35 50,65" fill="white"></polygon>
                    <polygon points="35,35 65,35 50,65" fill="white"></polygon>
                    <polygon points="35,35 65,35 50,65" fill="white"></polygon>
                  </mask>
                </defs>
              </svg>
              <div class="box"></div>
            </div>
            Generating the best for you... Hold on!
        </div>
        <div class="skeleton-box skeleton-header"></div>
        <div class="skeleton-box skeleton-text"></div>
        <div class="skeleton-box skeleton-text" style="width: 90%;"></div>
        <div class="skeleton-box skeleton-img"></div>
        <div class="skeleton-box skeleton-text"></div>
        <div class="skeleton-box skeleton-text" style="width: 80%;"></div>
    </div>
    ''', unsafe_allow_html=True)
