#!/bin/bash

# Education Analytics Data Warehouse - Setup Script

set -e

echo "🚀 Setting up Education Analytics Data Warehouse..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.9+ is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)'; then
            print_success "Python $PYTHON_VERSION is installed"
        else
            print_error "Python 3.9+ is required. Current version: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if command -v docker &> /dev/null; then
        print_success "Docker is installed"
    else
        print_warning "Docker is not installed. You'll need Docker to run the database services."
        echo "Please install Docker from https://docs.docker.com/get-docker/"
    fi
}

# Check if Docker Compose is installed
check_docker_compose() {
    print_status "Checking Docker Compose installation..."
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose is installed"
    else
        print_warning "Docker Compose is not installed. You'll need it to run the database services."
        echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    if [ ! -f ".env" ]; then
        cp env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your configuration"
    else
        print_warning "Environment file already exists"
    fi
}

# Start database services
start_databases() {
    print_status "Starting database services..."
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d postgres mongodb redis
        print_success "Database services started"
        
        # Wait for services to be ready
        print_status "Waiting for services to be ready..."
        sleep 10
        
        # Check if services are running
        if docker-compose ps | grep -q "Up"; then
            print_success "Database services are running"
        else
            print_error "Failed to start database services"
            exit 1
        fi
    else
        print_warning "Docker Compose not available. Please start databases manually."
    fi
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    if [ -f "scripts/init_database.py" ]; then
        python scripts/init_database.py
        print_success "Database initialized"
    else
        print_warning "Database initialization script not found"
    fi
}

# Generate sample data
generate_sample_data() {
    print_status "Generating sample data..."
    if [ -f "data/sample_data.py" ]; then
        python data/sample_data.py
        print_success "Sample data generated"
    else
        print_warning "Sample data generation script not found"
    fi
}

# Main setup function
main() {
    echo "=========================================="
    echo "Education Analytics Data Warehouse Setup"
    echo "=========================================="
    echo
    
    # Check prerequisites
    check_python
    check_docker
    check_docker_compose
    
    # Setup Python environment
    create_venv
    activate_venv
    install_dependencies
    
    # Setup configuration
    create_env_file
    
    # Start services
    start_databases
    
    # Initialize database
    init_database
    
    # Generate sample data
    generate_sample_data
    
    echo
    echo "=========================================="
    print_success "Setup completed successfully!"
    echo "=========================================="
    echo
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Start the application: python run.py"
    echo "3. Open http://localhost:8000/docs for API documentation"
    echo "4. Open http://localhost:8000/dashboard for the interactive dashboard"
    echo
    echo "For more information, see the documentation in the docs/ directory"
    echo
}

# Run main function
main "$@"
