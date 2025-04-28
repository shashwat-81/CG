#include <GL/glut.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

const int windowWidth = 600, windowHeight = 800;
const int carWidth = 50, carHeight = 100;
const int laneWidth = 100;

int carPosX = 250;       // Player car position
int carSpeed = 20;

struct Enemy {
    int x, y, speed;
};

const int maxEnemies = 3;
Enemy enemies[maxEnemies];

bool gameOver = false;
bool isPaused = false;
int score = 0;
int enemyBaseSpeed = 5;

void resetEnemies() {
    for (int i = 0; i < maxEnemies; i++) {
        enemies[i].x = 150 + (rand() % 4) * laneWidth;
        enemies[i].y = windowHeight + rand() % 300;
        enemies[i].speed = enemyBaseSpeed + rand() % 3;
    }
}

void resetGame() {
    carPosX = 250;
    score = 0;
    gameOver = false;
    isPaused = false;
    enemyBaseSpeed = 5;
    resetEnemies();
}

void drawText(float x, float y, const char* text, void* font = GLUT_BITMAP_HELVETICA_18) {
    glRasterPos2f(x, y);
    for (const char* c = text; *c != '\0'; c++) {
        glutBitmapCharacter(font, *c);
    }
}

void drawCar(int x, int y, float r, float g, float b) {
    glColor3f(r, g, b);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(x + carWidth, y);
    glVertex2f(x + carWidth, y + carHeight);
    glVertex2f(x, y + carHeight);
    glEnd();
}

void drawRoad() {
    glColor3f(0.3, 0.3, 0.3); // Dark grey road
    glBegin(GL_QUADS);
    glVertex2f(100, 0);
    glVertex2f(500, 0);
    glVertex2f(500, windowHeight);
    glVertex2f(100, windowHeight);
    glEnd();

    // Draw lane lines
    glColor3f(1, 1, 1);
    for (int y = 0; y < windowHeight; y += 80) {
        glBegin(GL_QUADS);
        glVertex2f(195, y);
        glVertex2f(205, y);
        glVertex2f(205, y + 40);
        glVertex2f(195, y + 40);
        glEnd();

        glBegin(GL_QUADS);
        glVertex2f(295, y);
        glVertex2f(305, y);
        glVertex2f(305, y + 40);
        glVertex2f(295, y + 40);
        glEnd();

        glBegin(GL_QUADS);
        glVertex2f(395, y);
        glVertex2f(405, y);
        glVertex2f(405, y + 40);
        glVertex2f(395, y + 40);
        glEnd();
    }
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    drawRoad();

    if (!gameOver) {
        // Draw player's car
        drawCar(carPosX, 50, 0.0, 0.0, 1.0);

        // Draw enemy cars
        for (int i = 0; i < maxEnemies; i++) {
            drawCar(enemies[i].x, enemies[i].y, 1.0, 0.0, 0.0);
        }

        // Display score
        glColor3f(1, 1, 0);
        char scoreStr[20];
        sprintf(scoreStr, "Score: %d", score);
        drawText(10, 770, scoreStr);
    }
    else {
        glColor3f(1, 0, 0);
        drawText(220, 400, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24);

        glColor3f(1, 1, 0);
        char scoreStr[30];
        sprintf(scoreStr, "Final Score: %d", score);
        drawText(210, 360, scoreStr);

        drawText(160, 320, "Press 'R' to Restart", GLUT_BITMAP_HELVETICA_18);
    }

    glutSwapBuffers();
}

bool checkCollision(int carX, int carY, int enemyX, int enemyY) {
    return !(carX + carWidth < enemyX || carX > enemyX + carWidth ||
             carY + carHeight < enemyY || carY > enemyY + carHeight);
}

void timer(int) {
    if (!gameOver && !isPaused) {
        for (int i = 0; i < maxEnemies; i++) {
            enemies[i].y -= enemies[i].speed;

            if (enemies[i].y < -carHeight) {
                enemies[i].y = windowHeight + rand() % 300;
                enemies[i].x = 150 + (rand() % 4) * laneWidth;
                enemies[i].speed = enemyBaseSpeed + rand() % 3;
                score++;

                // Increase difficulty
                if (score % 10 == 0) {
                    enemyBaseSpeed++;
                }
            }

            if (checkCollision(carPosX, 50, enemies[i].x, enemies[i].y)) {
                gameOver = true;
            }
        }
        glutPostRedisplay();
    }
    glutTimerFunc(16, timer, 0);
}

void specialKeys(int key, int, int) {
    if (!gameOver && !isPaused) {
        if (key == GLUT_KEY_LEFT && carPosX > 150) {
            carPosX -= carSpeed;
        }
        if (key == GLUT_KEY_RIGHT && carPosX < 450) {
            carPosX += carSpeed;
        }
    }
}

void keyboard(unsigned char key, int, int) {
    if (key == 'r' || key == 'R') {
        resetGame();
    }
    if (key == 'p' || key == 'P') {
        isPaused = !isPaused;
    }
    if (key == 27) { // ESC key
        exit(0);
    }
}

void init() {
    glClearColor(0.7, 0.8, 0.9, 1.0); // Sky blue background
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, windowWidth, 0, windowHeight);
    glMatrixMode(GL_MODELVIEW);
    srand(time(NULL));
    resetEnemies();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(windowWidth, windowHeight);
    glutCreateWindow("Racing Gems - Advanced Version");

    init();
    glutDisplayFunc(display);
    glutSpecialFunc(specialKeys);
    glutKeyboardFunc(keyboard);
    glutTimerFunc(0, timer, 0);

    glutMainLoop();
    return 0;
}
