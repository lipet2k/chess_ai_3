/**
 * Source: React Strap Examples
 */
import React from 'react'
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem } from 'reactstrap';

class Navigation extends React.Component {
    constructor(props) {
        super(props);
    
        this.toggle = this.toggle.bind(this);
        this.state = {
          isOpen: false
        };
      }
      toggle() {
        this.setState({
          isOpen: !this.state.isOpen
        });
      }


    render() {
        return (

            
<div className='nav'>

<Navbar color="light" light expand="md">
          <NavbarBrand href="#">Li-Marin Chess Engine</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href="#">Github</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="#">Paper</NavLink>
              </NavItem>
              <UncontrolledDropdown nav inNavbar>
                <DropdownToggle nav caret>
                  Search Options
                </DropdownToggle>
                <DropdownMenu right>

                  <DropdownItem>
                    MiniMax Search
                  </DropdownItem>

                  <DropdownItem divider />
                  <DropdownItem>
                    Alpha Beta Pruning
                  </DropdownItem>

                  <DropdownItem divider />
                  <DropdownItem>
                    Logistic Regression
                  </DropdownItem>
                </DropdownMenu>
              </UncontrolledDropdown>
            </Nav>
          </Collapse>
        </Navbar>
            </div>
        );
    }
}

export default Navigation;