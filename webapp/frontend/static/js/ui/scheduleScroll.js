export default function(){
    const raceSchedulueContainer = document.querySelector(".raceScheduleContainer");
    const arrowButtons = document.querySelectorAll(".raceScheduleButton");
    const firstCardWidth = raceSchedulueContainer.querySelector(".raceSchedule").offsetWidth;
    const scheduleDeadEnd = raceSchedulueContainer.querySelector(".scheduleDeadEnd .text").offsetWidth;
    
    const stopArrowButtonOpacityBreath = () => {
        arrowButtons.forEach(btn => {
            btn.style.animation = 'none';
        })
    };


    arrowButtons.forEach(btn =>{
        btn.addEventListener("mousedown", ()=>{
            isButtonArrowClick = true;
            });
        btn.addEventListener("click", () =>{
            if(btn.id === "right"){
                raceSchedulueContainer.scrollLeft += firstCardWidth 
            }else if(btn.id === "left"){
                raceSchedulueContainer.scrollLeft -= firstCardWidth
            }
            restartScroll()
        })
        btn.addEventListener("mousemove",stopArrowButtonOpacityBreath)
    })


    let isDragging = false,isButtonArrowClick = false, startX, startScrollLeft;

    const dragStart = (e) =>{ 
        isDragging = true;
        if (!isButtonArrowClick){
            startX = e.pageX;
            startScrollLeft = raceSchedulueContainer.scrollLeft;
        }
        restartScroll()
        
    }

    const dragStop = ()=> {
        isButtonArrowClick = false;
        isDragging = false;
        raceSchedulueContainer.classList.remove("dragging");
        restartScroll()
    }

    const dragging = (e) =>{
        if(!isDragging || isButtonArrowClick) return
        raceSchedulueContainer.classList.add("dragging");
        raceSchedulueContainer.scrollLeft = startScrollLeft - (e.pageX - startX);
    }

    const restartScroll = () => {
        if(raceSchedulueContainer.scrollLeft >= raceSchedulueContainer.scrollWidth - raceSchedulueContainer.offsetWidth - firstCardWidth + scheduleDeadEnd && !isDragging){
            raceSchedulueContainer.scrollLeft = 0;
        }
    }

    raceSchedulueContainer.addEventListener("mousedown", dragStart);
    document.addEventListener("mousemove", dragging);
    document.addEventListener("mouseup", dragStop);
    raceSchedulueContainer.addEventListener("scroll", restartScroll)
    
}