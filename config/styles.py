MUSE_COLORS = {
    "Lunes": "#5783A6",
    "Ares": "#D54D2E",
    "Rabu": "#8CB07F",
    "Thunor": "#F8D86A",
    "Shukra": "#5E47A1",
    "Dosei": "#7F49A2",
    "Solis": "#D48348"
}

MUSE_FONTS = {
    "Lunes": "#FBFBFB",
    "Ares": "#000000",
    "Rabu": "#000000",
    "Thunor": "#FFFFFF",
    "Shukra": "#FFFFFF",
    "Dosei": "#FFFFFF",
    "Solis": "#000000"    
}

def get_cosmic_css(muse_name: str) -> str:
    color = MUSE_COLORS.get(muse_name, "#7F49A2")
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
        
        body {{
            background: linear-gradient(135deg, #2a1a4a 0%, {color} 100%);
            margin: 0;
            justify-content: center;
            align-items: center;
            font-family: 'Cormorant Garamond', serif;
            color: #d1c4e9;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
            box-sizing: border-box;
        }}

        .cosmic-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background:
                radial-gradient(circle at 30% 50%, {color}33 0%, transparent 30%),
                radial-gradient(circle at 80% 70%, {color}44 0%, transparent 25%),
                linear-gradient(to bottom, #2a1a4a, #5E47A1);
        }}

        .static-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, 
                rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px),
                repeating-linear-gradient(90deg, rgba(0,0,0,0.15) 0px, 
                rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
            opacity: 0.2;
            z-index: -1;
            pointer-events: none;
            animation: static 0.2s infinite;
        }}

        @keyframes static {{
            0% {{ background-position: 0 0; }}
            100% {{ background-position: 3px 3px; }}
        }}

        .particle {{
            position: absolute;
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            pointer-events: none;
        }}
    </style>
    """

def get_particle_js() -> str:
    return """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            function createParticle() {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                const size = Math.random() * 3 + 1;
                const posX = Math.random() * window.innerWidth;
                const posY = Math.random() * window.innerHeight;
                const opacity = Math.random() * 0.5 + 0.1;
                const color = `rgba(16, 16, 16, ${opacity})`;
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${posX}px`;
                particle.style.top = `${posY}px`;
                particle.style.opacity = opacity;
                
                document.body.appendChild(particle);
                animateParticle(particle);
            }

            function animateParticle(particle) {
                let x = parseFloat(particle.style.left);
                let y = parseFloat(particle.style.top);
                const speedX = (Math.random() - 0.5) * 0.5;
                const speedY = (Math.random() - 0.5) * 0.5;
                
                function move() {
                    x += speedX;
                    y += speedY;
                    
                    if (x < 0 || x > window.innerWidth || y < 0 || y > window.innerHeight) {
                        x = Math.random() * window.innerWidth;
                        y = Math.random() * window.innerHeight;
                    }
                    
                    particle.style.left = `${x}px`;
                    particle.style.top = `${y}px`;
                    requestAnimationFrame(move);
                }
                
                move();
            }

            for (let i = 0; i < 30; i++) {
                createParticle();
            }
        });
    </script>
    """