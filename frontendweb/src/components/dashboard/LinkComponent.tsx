import React from 'react'
import Link from "next/link";

const LinkComponent = () => {
  return (
    <li>
      <Link
        className={`flex space-x-4 w-20 justify-center items-center p-1 text-gray-800 font-medium rounded-lg hover:bg-ewe-50 hover:text-gray-500 transition-colors duration-200`}
        href=""
      >
        This is a link
      </Link>
    </li>
  )
}

export default LinkComponent