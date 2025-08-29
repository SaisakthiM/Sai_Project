document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Loader Animation ---
    const loaderOverlay = document.getElementById('loader-overlay');
    const loaderLeft = document.getElementById('loader-left');
    const loaderRight = document.getElementById('loader-right');
    const loaderCounter = document.getElementById('loader-counter');
    const mainContent = document.getElementById('main-content');

    let count = 0;
    const counterInterval = setInterval(() => {
        if (count < 100) {
            count++;
            loaderCounter.textContent = `${count}%`;
        }
    }, 10);

    // GSAP Timeline for the loader
    const loaderTL = gsap.timeline({
        onComplete: () => {
            clearInterval(counterInterval);
            loaderOverlay.style.display = 'none';
        }
    });

    loaderTL
        .to([loaderLeft, loaderRight], {
            scaleX: 1.66,
            duration: 1,
            ease: 'power3.inOut'
        })
        .to(loaderCounter, {
            opacity: 0,
            duration: 0.3
        }, "<")
        .to(loaderLeft, {
            x: '-100%',
            duration: 1,
            ease: 'power3.inOut'
        })
        .to(loaderRight, {
            x: '100%',
            duration: 1,
            ease: 'power3.inOut'
        }, "<")
        .to(mainContent, {
            opacity: 1,
            duration: 1,
            ease: 'power2.in'
        }, "-=0.5");


    // --- 2. Custom Cursor ---
    const cursorDot = document.getElementById('cursor-dot');
    const cursorOutline = document.getElementById('cursor-outline');
    const hoverables = document.querySelectorAll('a, button, .cta-btn, .nav-link, .project-card');

    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let outlineX = 0, outlineY = 0;

    gsap.to({}, {
        repeat: -1,
        onUpdate: () => {
            dotX = gsap.utils.interpolate(dotX, mouseX, 0.2);
            dotY = gsap.utils.interpolate(dotY, mouseY, 0.2);
            outlineX = gsap.utils.interpolate(outlineX, mouseX, 0.1);
            outlineY = gsap.utils.interpolate(outlineY, mouseY, 0.1);

            gsap.set(cursorDot, { x: dotX, y: dotY });
            gsap.set(cursorOutline, { x: outlineX, y: outlineY });
        }
    });

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    hoverables.forEach(el => {
        el.addEventListener('mouseenter', () => {
            gsap.to(cursorDot, { scale: 0.2, duration: 0.3 });
            gsap.to(cursorOutline, { scale: 1.5, borderColor: '#4f46e5', duration: 0.3 });
        });
        el.addEventListener('mouseleave', () => {
            gsap.to(cursorDot, { scale: 1, duration: 0.3 });
            gsap.to(cursorOutline, { scale: 1, borderColor: '#fff', duration: 0.3 });
        });
    });

    // --- 3. GSAP Animations & ScrollTriggers ---
    gsap.registerPlugin(ScrollTrigger);

    // Navbar shrink on scroll
    gsap.to('#navbar', {
        paddingTop: '1rem',
        paddingBottom: '1rem',
        backgroundColor: 'rgba(17,24,39,0.7)',
        backdropFilter: 'blur(10px)',
        scrollTrigger: {
            trigger: 'body',
            start: 'top -80px', // When user scrolls 80px down
            end: 'top -81px',
            toggleActions: 'play none none reverse',
            scrub: true
        }
    });

    // Hero Text Fade In
    gsap.fromTo('.hero-text', { y: 20, opacity: 0 }, {
        y: 0,
        opacity: 1,
        stagger: 0.2,
        duration: 1.5,
        ease: 'power3.out'
    });

    // About Section Fade In
    gsap.utils.toArray('.about-image-reveal, .about-text-reveal').forEach(el => {
        gsap.from(el, {
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: el,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });
    });
    
    // Experience Timeline fade in
    gsap.utils.toArray('.timeline-item').forEach(el => {
        gsap.from(el, {
            x: el.classList.contains('timeline-right') ? 50 : -50,
            opacity: 0,
            duration: 1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: el,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });
    });

    // Education fade in
    gsap.utils.toArray('.education-card').forEach(el => {
        gsap.from(el, {
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: el,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });
    });


    // Horizontal Scroll Projects Section
    const projectsContainer = document.getElementById('projects-container');
    const projectsCards = document.querySelectorAll('.project-card');

    gsap.to(projectsCards, {
        xPercent: -100 * (projectsCards.length - 1),
        ease: 'none',
        scrollTrigger: {
            trigger: '#projects',
            pin: true,
            scrub: 1,
            end: () => `+=${projectsContainer.offsetWidth}`
        }
    });

    // Circle Text Rotation
    gsap.to('#circle-text', {
        rotation: 360,
        duration: 40,
        ease: 'linear',
        repeat: -1
    });

    // --- 4. Mobile Menu Toggle ---
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('translate-x-full');
    });

    document.querySelectorAll('#mobile-menu a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('translate-x-full');
        });
    });


    // --- 5. Three.js Starfield Background ---
    const canvas = document.getElementById('bg-starfield');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
    
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.position.z = 50;

    const particlesGeometry = new THREE.BufferGeometry();
    const particleCount = 5000;
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i++) {
        positions[i] = (Math.random() - 0.5) * 200;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particlesMaterial = new THREE.PointsMaterial({
        color: 0x4c51bf,
        size: 0.8,
        transparent: true,
        blending: THREE.AdditiveBlending,
        opacity: 0.6
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Mouse Parallax
    let mouseX_3d = 0;
    let mouseY_3d = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX_3d = (e.clientX / window.innerWidth) - 0.5;
        mouseY_3d = (e.clientY / window.innerHeight) - 0.5;
    });

    function animate() {
        requestAnimationFrame(animate);

        // Slow rotation
        particlesMesh.rotation.x += 0.0001;
        particlesMesh.rotation.y += 0.0002;

        // Camera Parallax
        camera.position.x += (mouseX_3d * 20 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY_3d * 20 - camera.position.y) * 0.02;

        renderer.render(scene, camera);
    }
    
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

});