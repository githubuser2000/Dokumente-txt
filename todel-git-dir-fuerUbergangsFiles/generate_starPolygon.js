"use strict";
class StarPolygon {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.context = this.canvas.getContext('2d');
    }
    drawStarPolygon(n, centerX, centerY, radius, startAngle = 0) {
        if (n < 5) {
            console.log("Cannot draw a star polygon with less than 5 points");
            return;
        }
        let angleStep = Math.PI * 2 / n;
        this.context.beginPath();
        for (let i = 0; i <= 2 * n; i++) {
            let radiusForPoint = (i % 2 === 0) ? radius : radius / 2;
            let angle = i * angleStep / 2 + startAngle;
            let x = centerX + radiusForPoint * Math.cos(angle);
            let y = centerY + radiusForPoint * Math.sin(angle);
            if (i === 0) {
                this.context.moveTo(x, y);
            }
            else {
                this.context.lineTo(x, y);
            }
        }
        this.context.closePath();
        this.context.stroke();
    }
}
window.onload = () => {
    let polygon = new StarPolygon('myCanvas');
    polygon.drawStarPolygon(5, 100, 100, 50); // Draw a 5-pointed star
    polygon.drawStarPolygon(6, 200, 200, 50); // Draw a 6-pointed star
    polygon.drawStarPolygon(7, 300, 300, 50); // Draw a 7-pointed star
};
