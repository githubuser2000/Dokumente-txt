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
        for (let i = 0; i < n; i++) {
            let angle1 = i * angleStep + startAngle;
            let x1 = centerX + radius * Math.cos(angle1);
            let y1 = centerY + radius * Math.sin(angle1);
            let j = (i + 3) % n;
            let angle2 = j * angleStep + startAngle;
            let x2 = centerX + radius * Math.cos(angle2);
            let y2 = centerY + radius * Math.sin(angle2);
            this.context.moveTo(x1, y1);
            this.context.lineTo(x2, y2);
        }
        this.context.stroke();
    }
}
window.onload = () => {
    let polygon = new StarPolygon('myCanvas');
    polygon.drawStarPolygon(8, 100, 100, 50); // Draw a 5-pointed star
    polygon.drawStarPolygon(9, 100, 300, 50); // Draw a 6-pointed star
    polygon.drawStarPolygon(7, 300, 100, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(10, 300, 300, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(11, 500, 100, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(12, 100, 500, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(13, 500, 500, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(14, 300, 500, 50); // Draw a 7-pointed star
    polygon.drawStarPolygon(15, 500, 300, 50); // Draw a 7-pointed star
};
