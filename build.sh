#!/bin/bash
#
# Plex Lifecycle Manager - Build & Deploy Script
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║         Plex Lifecycle Manager - Build Script              ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
echo -e "${GREEN}✓ Docker Compose found: $(docker-compose --version)${NC}"
echo ""

# Menu
echo "What would you like to do?"
echo ""
echo "  1) Build and start container"
echo "  2) Stop container"
echo "  3) Rebuild container (no cache)"
echo "  4) View logs"
echo "  5) Open shell in container"
echo "  6) Clean up (remove container and volumes)"
echo "  7) Check status"
echo "  8) Exit"
echo ""
read -p "Choose an option [1-8]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Building and starting container...${NC}"
        docker-compose up -d --build
        echo ""
        echo -e "${GREEN}✓ Container started!${NC}"
        echo ""
        echo "Access Web UI at: http://localhost:8765"
        echo ""
        ;;
    2)
        echo ""
        echo -e "${BLUE}Stopping container...${NC}"
        docker-compose down
        echo ""
        echo -e "${GREEN}✓ Container stopped${NC}"
        ;;
    3)
        echo ""
        echo -e "${YELLOW}⚠ This will rebuild the container from scratch${NC}"
        read -p "Continue? [y/N]: " confirm
        if [[ $confirm == "y" || $confirm == "Y" ]]; then
            echo ""
            echo -e "${BLUE}Rebuilding container...${NC}"
            docker-compose down
            docker-compose build --no-cache
            docker-compose up -d
            echo ""
            echo -e "${GREEN}✓ Container rebuilt and started!${NC}"
        fi
        ;;
    4)
        echo ""
        echo -e "${BLUE}Showing logs (Ctrl+C to exit)...${NC}"
        echo ""
        docker-compose logs -f
        ;;
    5)
        echo ""
        echo -e "${BLUE}Opening shell in container...${NC}"
        echo ""
        docker exec -it plex-lifecycle bash
        ;;
    6)
        echo ""
        echo -e "${RED}⚠ WARNING: This will remove the container and ALL data${NC}"
        echo -e "${RED}   (config, reports, logs will be deleted!)${NC}"
        read -p "Are you absolutely sure? [y/N]: " confirm
        if [[ $confirm == "y" || $confirm == "Y" ]]; then
            echo ""
            echo -e "${BLUE}Cleaning up...${NC}"
            docker-compose down -v
            echo ""
            echo -e "${GREEN}✓ Cleanup complete${NC}"
        fi
        ;;
    7)
        echo ""
        echo -e "${BLUE}Container status:${NC}"
        echo ""
        docker-compose ps
        echo ""
        echo -e "${BLUE}Health check:${NC}"
        curl -s http://localhost:8765/health | python3 -m json.tool || echo "Container not responding"
        ;;
    8)
        echo ""
        echo -e "${GREEN}Bye!${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
