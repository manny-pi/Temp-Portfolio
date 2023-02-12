
function main() {
    // Get all the children in the skills section
    const skills_section = document.querySelector('.skills-section-wrapper').childNodes; 

    // 
    skills_section.forEach((item) => {
        
        // Execute when the user's pointer is over the software-development-section
        item.addEventListener('pointerover', () => {
            // Change the color of the div's border to white
            item.style.borderColor = 'black';
        });
        
        // Execute when the user's pointer leaves the software-development-section
        item.addEventListener('pointerout', () => {
            // Change the color of the div's border to white
            item.style.borderColor = 'white';
        });

        item.addEventListener('click', () => {
            console.log(`Go to ${item.dataset.url}`); 
            window.open(`${item.dataset.url}`);
        }); 
    });
}
document.addEventListener('DOMContentLoaded', () => main())