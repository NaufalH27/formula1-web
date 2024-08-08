import abstractView from "./abstractView.js";

export default class extends abstractView {
    constructor(){
        super();
        this.setTitle("Page Not Found")
    }

    async getHtml(){
        return `
        <h1> Page Not Found </h1>
        `;
    }
}