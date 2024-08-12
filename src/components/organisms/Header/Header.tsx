/**
 * Contains navigation, user login status, page search bar
 * @returns
 */
import "./Header.scss";
import ServerStatus from "../../atoms/ServerStatus/ServerStatus";
const Header = () => {
  return (
    <div className="header">
      <ServerStatus />
    </div>
  );
};

export default Header;
