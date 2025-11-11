class StarPolygon {
    private canvas: HTMLCanvasElement;
    private context: CanvasRenderingContext2D;

    constructor(canvasId: string) {
        this.canvas = document.getElementById(canvasId) as HTMLCanvasElement;
        this.context = this.canvas.getContext('2d');
    }

    drawPolygon(n: number, centerX: number, centerY: number, radius: number, startAngle: number = 0) {
        if (n < 2) {
            console.log("Cannot draw a polygon with less than 2 sides");
            return;
        }

        let angleStep = Math.PI * 2 / n;
        this.context.beginPath();

        for (let i = 0; i <= n; i++) {
            let angle = i * angleStep + startAngle;
            let x = centerX + radius * Math.cos(angle);
            let y = centerY + radius * Math.sin(angle);
            if (i === 0) {
                this.context.moveTo(x, y);
            } else {
                this.context.lineTo(x, y);
            }
        }

        this.context.closePath();
        this.context.stroke();
    }
}

window.onload = () => {
    let polygon = new StarPolygon('myCanvas');
    polygon.drawPolygon(3, 100, 100, 50); // Draw a triangle
    polygon.drawPolygon(4, 200, 200, 50); // Draw a square
    polygon.drawPolygon(5, 300, 300, 50); // Draw a pentagon
    polygon.drawPolygon(1, 400, 400, 50); // Draw a line
    polygon.drawPolygon(0, 500, 500, 50); // Draw a point
};
