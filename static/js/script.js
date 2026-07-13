// =========================================
// TOOLHUB 2.0
// Professional JavaScript
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    // ===========================
    // Card Hover Animation
    // ===========================

    const cards = document.querySelectorAll(".tool-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-12px) scale(1.03)";
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0px) scale(1)";
        });

    });


    // ===========================
    // Button Click Animation
    // ===========================

    const buttons = document.querySelectorAll(".btn, button");

    buttons.forEach(button => {

        button.addEventListener("click", function () {

            button.style.transform = "scale(.95)";

            setTimeout(() => {

                button.style.transform = "scale(1)";

            },150);

        });

    });


    // ===========================
    // Loading Spinner
    // ===========================

    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", function(){

            const loader=document.getElementById("loader");

            if(loader){

                loader.style.display="flex";

            }

            const progress=document.getElementById("progress-container");

            const bar=document.getElementById("progress-bar");

            if(progress){

                progress.style.display="block";

                let width=0;

                const interval=setInterval(function(){

                    if(width>=95){

                        clearInterval(interval);

                    }

                    else{

                        width++;

                        bar.style.width=width+"%";

                    }

                },40);

            }

        });

    });


    // ===========================
    // Smooth Scroll
    // ===========================

    document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

        anchor.addEventListener("click",function(e){

            e.preventDefault();

            const target=document.querySelector(this.getAttribute("href"));

            if(target){

                target.scrollIntoView({

                    behavior:"smooth"

                });

            }

        });

    });


    // ===========================
    // Fade In Cards
    // ===========================

    const observer = new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.style.opacity="1";

                entry.target.style.transform="translateY(0px)";

            }

        });

    });

    document.querySelectorAll(".tool-card,.tool-container").forEach(el=>{

        el.style.opacity="0";

        el.style.transform="translateY(40px)";

        el.style.transition=".8s";

        observer.observe(el);

    });

});



// =====================================
// Universal File Upload
// =====================================
const fileInput = document.getElementById("fileInput");
const filename = document.getElementById("filename");
const filesize = document.getElementById("filesize");

if(fileInput){

    fileInput.addEventListener("change",function(){

        if(this.files.length===0){

            filename.innerHTML="No file selected";
            filesize.innerHTML="";
            return;

        }

        if(this.files.length===1){

            const file=this.files[0];

            filename.innerHTML="✅ "+file.name;

            filesize.innerHTML=
            "Size : "+(file.size/1024/1024).toFixed(2)+" MB";

        }

        else{

            filename.innerHTML=
            "✅ "+this.files.length+" files selected";

            let total=0;

            for(let file of this.files){

                total+=file.size;

            }

            filesize.innerHTML=
            "Total Size : "+(total/1024/1024).toFixed(2)+" MB";

        }

    });

}


// =====================================
// Animated Statistics
// =====================================

function animateCounter(id, target, suffix = "") {

    const element = document.getElementById(id);

    if (!element) return;

    let value = 0;

    const timer = setInterval(() => {

        value++;

        element.textContent = value + suffix;

        if (value >= target) {

            clearInterval(timer);

        }

    }, 30);

}

window.addEventListener("load", () => {

    animateCounter("toolsCounter", 25, "+");

    animateCounter("freeCounter", 100, "%");

    animateCounter("speedCounter", 99, "%");

    document.getElementById("secureCounter").textContent = "100%";

});

// =====================================
// Tool Search
// =====================================

const searchInput = document.getElementById("toolSearch");

if(searchInput){

    searchInput.addEventListener("keyup",function(){

        const value=this.value.toLowerCase();

        document.querySelectorAll(".card").forEach(card=>{

            const text=card.innerText.toLowerCase();

            if(text.includes(value)){

                card.style.display="block";

            }

            else{

                card.style.display="none";

            }

        });

    });

}