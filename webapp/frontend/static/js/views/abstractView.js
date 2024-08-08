export default class{
    constructor(){
        
    }
    setTitle(title){
        document.title = title;
    }
    async getHtml() {
        return "";
    }
    getCurrentYear(){
        const date = new Date();
        return date.getFullYear()
    }
}




